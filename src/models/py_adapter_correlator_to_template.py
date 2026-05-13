"""
Adapter: correlation data → domain inference and template selection.
Imported by py_skill_job_correlator after facets are computed.
"""

import json
from pathlib import Path
from typing import Dict, List

from src.utils.logging_manager import get_logger

_logger = get_logger('resume-machine.adapter')

_FEATURED_LANGUAGES = {
    'python', 'javascript', 'typescript', 'go', 'java',
    'rust', 'c++', 'bash', 'ruby', 'php',
}
_SQL_EXACT = 'sql'

_template_cache: Dict[str, List[dict]] = {}

DEFAULT_DOMAIN = 'fullstack'


def _load_templates(role_templates_dir: str) -> List[dict]:
    if role_templates_dir in _template_cache:
        return _template_cache[role_templates_dir]

    templates_path = Path(role_templates_dir)
    files = sorted(templates_path.glob('*-resume.json'))
    if not files:
        raise FileNotFoundError(
            f'No role template JSON files found in: {role_templates_dir}'
        )

    templates = []
    for f in files:
        with open(f) as fh:
            templates.append(json.load(fh))
    _template_cache[role_templates_dir] = templates
    _logger.debug('Loaded %d role templates from %s', len(templates), role_templates_dir)
    return templates


def infer_domain(correlation_data: dict, role_templates_dir: str) -> dict:
    templates = _load_templates(role_templates_dir)
    correlation_terms = {
        entry['term'].lower()
        for entry in correlation_data.get('correlations', [])
    }

    scores: Dict[str, int] = {}
    for tmpl in templates:
        domain = tmpl.get('domain', '')
        keywords = {kw.lower() for kw in tmpl.get('keywords', [])}
        scores[domain] = sum(1 for t in correlation_terms if t in keywords)

    best_score = max(scores.values(), default=0)
    if best_score == 0:
        winning_domain = DEFAULT_DOMAIN
    else:
        candidates = [d for d, s in scores.items() if s == best_score]
        winning_domain = sorted(candidates)[0]

    winning_tmpl = next(
        (t for t in templates if t.get('domain') == winning_domain), None
    )
    highlights = (winning_tmpl.get('highlights', [])[:6]) if winning_tmpl else []

    featured_languages: List[str] = []
    for entry in correlation_data.get('correlations', []):
        term = entry.get('term', '')
        term_lower = term.lower()
        if term_lower == _SQL_EXACT:
            featured_languages.append(term)
        elif term_lower in _FEATURED_LANGUAGES:
            featured_languages.append(term)

    seen: set = set()
    deduped: List[str] = []
    for lang in featured_languages:
        key = lang.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(lang)

    _logger.debug(
        'Domain inferred: %s (score=%d), languages=%s',
        winning_domain, best_score, deduped
    )

    return {
        'domain': winning_domain,
        'featured_languages': deduped,
        'highlights': highlights,
    }
