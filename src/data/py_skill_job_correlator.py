"""
Skill–job correlator.

Reads a job JSON, correlates required/additional skills against the v2.3.0
facet_catalog in skills-index.json, writes:
  - resume-{candidate}-{employer}-{title}.json  (always overwritten)
  - letter-{candidate}-{employer}-{title}.json  (written only if absent)

Usage:
  python -m src.data.py_skill_job_correlator <job_json_path> [--name <candidate>]
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from src.utils.logging_manager import get_logger, set_level
from src.utils.config_manager import load_config
from src.utils.naming_utils import slugify, correlation_json_path, cover_letter_json_path, employer_short_slug
from src.models.py_adapter_correlator_to_template import infer_domain

_logger = get_logger('resume-machine.correlator')

_STALENESS_MONTHS = 24

_LEAD_EXPERIENCE_LEVELS = {'advanced', 'expert'}
_LEAD_PROFICIENCIES = {'expert'}
_SOLID_EXPERIENCE_LEVELS = {'intermediate'}
_SOLID_PROFICIENCIES = {'intermediate', 'proficient'}
_WEAK_EXPERIENCE_LEVELS = {'beginner'}
_WEAK_PROFICIENCIES = {'novice', 'beginner'}


def _build_facet_lookup(skills_index: dict) -> dict[str, dict]:
    facet_lookup: dict[str, dict] = {}

    for entry in skills_index.get('facet_catalog', []):
        key = entry.get('facet_name', '').lower().strip()
        if not key:
            continue
        facet_lookup[key] = {
            **entry,
            'proficiency': None,
            'confidence_level': None,
            'years_of_experience': None,
            'last_used': None,
            'experience_level': None,
        }

    for skill_group_list in skills_index.get('skills', {}).values():
        for skill_group in skill_group_list:
            for facet_data in skill_group.get('facets', {}).values():
                fname = facet_data.get('facet_name', '').lower().strip()
                if fname in facet_lookup:
                    facet_lookup[fname].update({
                        'proficiency': facet_data.get('proficiency'),
                        'confidence_level': facet_data.get('confidence_level'),
                        'years_of_experience': facet_data.get('years_of_experience'),
                        'last_used': facet_data.get('last_used'),
                        'experience_level': facet_data.get('experience_level'),
                    })

    return facet_lookup


def _is_stale(last_used_str: Optional[str], now: datetime) -> bool:
    if not last_used_str:
        return False
    try:
        raw = last_used_str.strip()
        if len(raw) == 7:
            raw += '-01'
        lu = datetime.fromisoformat(raw).replace(tzinfo=timezone.utc)
        months_ago = (now.year - lu.year) * 12 + (now.month - lu.month)
        return months_ago > _STALENESS_MONTHS
    except ValueError:
        return False


def _load_template_keywords(role_templates_dir: str) -> set[str]:
    keywords: set[str] = set()
    for path in Path(role_templates_dir).glob('*-resume.json'):
        try:
            with open(path) as f:
                tmpl = json.load(f)
            for kw in tmpl.get('keywords', []):
                keywords.add(kw.lower())
        except Exception:
            pass
    return keywords


def _assign_tag(
    term: str,
    section: str,
    facet_entry: Optional[dict],
    template_keywords: set[str],
    now: datetime,
) -> Optional[str]:
    term_lower = term.lower()
    in_required = (section == 'required_skills')

    if facet_entry:
        stale = _is_stale(facet_entry.get('last_used'), now)
        exp = (facet_entry.get('experience_level') or '').lower()
        prof = (facet_entry.get('proficiency') or '').lower()

        if not in_required:
            return 'PARTIAL_MATCH'

        if stale:
            return 'UNTESTED_CLAIM'

        if exp in _LEAD_EXPERIENCE_LEVELS or prof in _LEAD_PROFICIENCIES:
            return 'LEAD_STRENGTH'
        if exp in _SOLID_EXPERIENCE_LEVELS or prof in _SOLID_PROFICIENCIES:
            return 'SOLID_MATCH'
        if exp in _WEAK_EXPERIENCE_LEVELS or prof in _WEAK_PROFICIENCIES:
            return 'UNTESTED_CLAIM'

        # facet exists but no proficiency/experience data — default SOLID_MATCH
        return 'SOLID_MATCH'

    # No facet match
    if term_lower in template_keywords:
        return 'GAP_ADJACENCY'

    if in_required:
        return 'HARD_GAP'

    # additional_skills with no match → silently excluded
    return None


def _infer_facet_type(facet_entry: Optional[dict], domain_facet_types: list[str]) -> str:
    if facet_entry:
        ft = facet_entry.get('facet_type', '')
        # Map internal facet_type to role-template-style category labels
        mapping = {
            'hands_on_language': 'language',
            'hands_on_framework': 'framework',
            'hands_on_tool': 'tool',
            'hands_on_platform': 'platform',
            'hands_on_skill': 'skill',
            'strategic_domain': 'domain',
            'leadership_soft_skill': 'leadership',
        }
        return mapping.get(ft, ft)
    return 'unknown'


def correlate_job(
    job_json_path_str: str,
    candidate_name: Optional[str] = None,
    dry_run: bool = False,
) -> dict:
    cfg = load_config()
    set_level(cfg.get('log_level', 'info'))

    candidate = slugify(candidate_name or cfg.get('candidate_name', 'candidate'))
    skills_index_path = cfg['skills_index_path']
    role_templates_dir = cfg['role_templates_dir']
    job_listings_dir = cfg['job-listings_dir']
    resume_source_path = cfg.get('resume_source_path', 'data/source/resume.source.json')
    letter_source_path = cfg.get('letter_source_path', 'data/source/letter.source.json')

    with open(resume_source_path) as f:
        resume_source = json.load(f)

    letter_source: dict = {}
    _letter_source_p = Path(letter_source_path)
    if _letter_source_p.exists():
        with open(_letter_source_p) as f:
            letter_source = json.load(f)
        _logger.debug('Loaded letter source: %s', letter_source_path)
    else:
        _logger.debug('No letter source found at %s; using built-in defaults', letter_source_path)

    job_json_path_obj = Path(job_json_path_str).resolve()
    with open(job_json_path_obj) as f:
        job_data = json.load(f)

    with open(skills_index_path) as f:
        skills_index = json.load(f)

    facet_lookup = _build_facet_lookup(skills_index)
    _logger.info('Loaded %d facets', len(facet_lookup))

    template_keywords = _load_template_keywords(role_templates_dir)

    employer = job_data.get('employer', 'unknown')
    job_title = job_data.get('job_title', 'unknown')
    location = job_data.get('location', '')

    jp = job_data.get('job_posting', {})
    required_skills: list[str] = jp.get('required_skills', [])
    additional_skills: list[str] = jp.get('additional_skills', [])

    now = datetime.now(timezone.utc)
    correlations: list[dict] = []
    seen_terms: set[str] = set()

    def _add_correlation(term: str, section: str) -> None:
        key = term.lower().strip()
        if not key or key in seen_terms:
            return
        seen_terms.add(key)

        facet_entry = facet_lookup.get(key)
        tag = _assign_tag(term, section, facet_entry, template_keywords, now)
        if tag is None:
            return

        corr_type = _infer_facet_type(facet_entry, [])
        notes = ''
        if facet_entry:
            parts = []
            if facet_entry.get('years_of_experience'):
                parts.append(f"{facet_entry['years_of_experience']}y exp")
            if facet_entry.get('last_used'):
                parts.append(f"last used {facet_entry['last_used']}")
            notes = ', '.join(parts)

        correlations.append({
            'term': term,
            'type': corr_type,
            'tag': tag,
            'notes': notes,
        })

    for term in required_skills:
        _add_correlation(term, 'required_skills')
    for term in additional_skills:
        _add_correlation(term, 'additional_skills')

    hard_gaps = [
        {'term': c['term'], 'context': 'required_skills'}
        for c in correlations if c['tag'] == 'HARD_GAP'
    ]
    tag_distribution: dict[str, int] = {}
    for c in correlations:
        tag_distribution[c['tag']] = tag_distribution.get(c['tag'], 0) + 1

    correlation_data: dict = {
        'metadata': {
            'job_title': job_title,
            'employer': employer,
            'location': location,
            'candidate_name': candidate,
            'generated_at': now.isoformat(),
            'job_json': str(job_json_path_obj),
            'skills_index': str(skills_index_path),
        },
        'summary': {
            'total_correlations': len(correlations),
            'hard_gaps_count': len(hard_gaps),
            'tag_distribution': tag_distribution,
        },
        'correlations': correlations,
        'hard_gaps': hard_gaps,
    }

    # Infer domain, languages, highlights
    adapter_result = infer_domain(correlation_data, role_templates_dir)
    correlation_data['domain'] = adapter_result['domain']
    correlation_data['featured_languages'] = adapter_result['featured_languages']
    correlation_data['highlights'] = adapter_result['highlights']

    # Derive output paths from job directory
    job_dir = job_json_path_obj.parent
    parts = job_dir.parts
    try:
        year, month, day = int(parts[-3]), int(parts[-2]), int(parts[-1])
    except (ValueError, IndexError):
        year, month, day = now.year, now.month, now.day

    job_slug = job_data.get('_slug') or slugify(f'{job_title} {location}'.strip())
    uid = job_data.get('_uid') or __import__('secrets').token_hex(3)
    emp_short = employer_short_slug(employer)

    corr_path = correlation_json_path(job_listings_dir, year, month, day, job_slug, emp_short, candidate, uid)
    letter_path = cover_letter_json_path(job_listings_dir, year, month, day, job_slug, emp_short, candidate, uid)

    if not dry_run:
        Path(corr_path).parent.mkdir(parents=True, exist_ok=True)
        with open(corr_path, 'w') as f:
            json.dump(correlation_data, f, indent=2)
        _logger.info('Wrote correlation: %s', corr_path)

        domain = correlation_data.get('domain', 'fullstack')
        letter_tmpl_path = Path(role_templates_dir) / f'{domain}-letter.json'
        # Start from the candidate default; domain file overrides non-empty fields.
        letter_tmpl: dict = dict(letter_source)
        if letter_tmpl_path.exists():
            with open(letter_tmpl_path) as f:
                domain_tmpl = json.load(f)
            for key in ('opening_template', 'closing_template', 'intro'):
                val = domain_tmpl.get(key)
                if val:
                    letter_tmpl[key] = val
        basics = resume_source.get('basics', {})
        letter = _build_cover_letter(correlation_data, employer, job_title, letter_tmpl, basics)
        with open(letter_path, 'w') as f:
            json.dump(letter, f, indent=2)
        _logger.info('Wrote cover letter: %s', letter_path)
    else:
        _logger.info('[dry-run] Would write correlation: %s', corr_path)
        _logger.info('[dry-run] Would write cover letter: %s', letter_path)

    return correlation_data


def _build_cover_letter(correlation_data: dict, employer: str, job_title: str, letter_tmpl: dict, basics: dict) -> dict:
    lead_strengths = [c for c in correlation_data['correlations'] if c['tag'] == 'LEAD_STRENGTH']
    highlights = correlation_data.get('highlights', [])

    if len(lead_strengths) >= 2:
        value_proposition = ' '.join(
            f"{c['term']} expertise brings proven impact." for c in lead_strengths[:2]
        )
    elif highlights:
        value_proposition = ' '.join(str(h) for h in highlights[:2])
    else:
        value_proposition = 'Extensive technical experience directly relevant to this role.'

    relevant_experience = highlights[:5] if highlights else []

    opening_tmpl = letter_tmpl.get(
        'opening_template',
        'Dear Hiring Team at {employer}, I am writing to apply for the {job_title} position.',
    )
    closing_tmpl = letter_tmpl.get(
        'closing_template',
        "I am currently based in Waterloo and can relocate if needed. I am excited about the possibility of contributing my communications and strategy experience to [organization’s] work and would welcome the chance to discuss the role further.",
    )
    intro = letter_tmpl.get('intro', '')

    signature = {
        'name': basics.get('name', ''),
        'title': basics.get('label', ''),
        'email': basics.get('email', ''),
        'phone': basics.get('phone', ''),
        'url': basics.get('url', ''),
    }

    return {
        'opening': opening_tmpl.format(employer=employer, job_title=job_title),
        'intro': intro,
        'value_proposition': value_proposition,
        'relevant_experience': relevant_experience,
        'closing': closing_tmpl.format(employer=employer),
        'signature': signature,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description='Correlate job JSON against skills index')
    parser.add_argument('job_json_path', help='Path to job JSON file')
    parser.add_argument('--name', dest='candidate_name', default=None,
                        help='Override candidate name (slugified before use)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print output paths without writing files')
    args = parser.parse_args(argv)

    try:
        correlate_job(
            args.job_json_path,
            candidate_name=args.candidate_name,
            dry_run=args.dry_run,
        )
        return 0
    except Exception as exc:
        _logger.error('Correlation failed: %s', exc, exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
