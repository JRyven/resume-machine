"""
HTML job posting extractor — pure Python, BeautifulSoup4 + lxml.
No Node.js, no browser automation.

Usage: python -m src.data.py_extract_jobs <input_dir>
"""

import json
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from src.utils.logging_manager import get_logger, set_level
from src.utils.config_manager import load_config
from src.utils.naming_utils import slugify, job_details_json_path, employer_short_slug

_logger = get_logger('resume-machine.ingest')


def _text(tag) -> str:
    return tag.get_text(strip=True) if tag else ''


def _list_items(ul) -> list[str]:
    if not ul:
        return []
    items = []
    for li in ul.find_all('li', recursive=False):
        spans = li.find_all('span')
        if spans:
            text = _text(spans[-1])
        else:
            text = _text(li)
        if text:
            items.append(text)
    return items


def extract_job_posting(html_path: Path) -> dict:
    with open(html_path, 'rb') as f:
        raw = f.read()
    soup = BeautifulSoup(raw.decode('utf-8', errors='replace'), 'lxml')

    output: dict = {}

    output['job_title'] = _text(soup.find('span', property='title'))
    output['employer'] = _text(soup.find('span', property='name'))
    _city   = _text(soup.find(property='addressLocality'))
    _region = _text(soup.find(property='addressRegion'))
    output['location'] = f'{_city}, {_region}' if _city and _region else _city or _region or _text(soup.find('span', property='address'))
    output['salary'] = _text(soup.find('span', property='value'))
    output['employment_type'] = _text(soup.find('span', property='employmentType'))

    # ── job_posting fields required by job_json_schema ─────────────────────────
    job_posting: dict = {
        'required_skills': [],
        'additional_skills': [],
        'responsibilities': [],
        'overview': '',
        'specialization': '',
    }

    # comparisonchart block → overview, languages, education, experience
    chart = soup.find('div', id='comparisonchart')
    if chart:
        lang_h4 = chart.find('h4', string='Languages')
        if lang_h4:
            lang_p = lang_h4.find_next_sibling('p')
            if lang_p:
                job_posting['specialization'] = _text(lang_p)

        exp_h4 = chart.find('h4', string='Experience')
        if exp_h4:
            exp_p = exp_h4.find_next_sibling('p')
            if exp_p:
                # collect non-invisible span text
                spans = exp_p.find_all('span')
                for s in spans:
                    classes = s.get('class') or []
                    if 'wb-inv' not in classes and not any('fa-' in c for c in classes):
                        t = _text(s)
                        if t:
                            job_posting['overview'] = t
                            break

    # jobOverview-2 → responsibilities
    resp_div = soup.find('div', id='jobOverview-2')
    if resp_div:
        all_items: list[str] = []
        for h4 in resp_div.find_all('h4'):
            ul = h4.find_next_sibling('ul')
            all_items.extend(_list_items(ul))
        job_posting['responsibilities'] = all_items

    # jobOverview-4 → skills classified by h4 category
    # Job Bank headings: "Computer and technology knowledge" → required
    # "Area of specialization", "Area of work experience" → additional
    _REQUIRED_CATEGORIES = {
        'computer and technology knowledge',
        'computer',
        'technology knowledge',
    }
    exp_div = soup.find('div', id='jobOverview-4')
    required_skills: list[str] = []
    additional_skills: list[str] = []
    if exp_div:
        for h4 in exp_div.find_all('h4'):
            category = _text(h4).lower()
            ul = h4.find_next_sibling('ul')
            items = _list_items(ul)
            if (
                any(cat in category for cat in _REQUIRED_CATEGORIES)
                or 'essential' in category
                or 'required' in category
            ):
                required_skills.extend(items)
            else:
                additional_skills.extend(items)

    job_posting['required_skills'] = required_skills
    job_posting['additional_skills'] = additional_skills

    output['job_posting'] = job_posting

    # extra fields from other sections (stored as-is, not consumed downstream)
    add_div = soup.find('div', id='jobOverview-5')
    if add_div:
        extras: dict = {}
        for h4 in add_div.find_all('h4'):
            cat = _text(h4)
            ul = h4.find_next_sibling('ul')
            items = _list_items(ul)
            if items:
                extras[cat] = items
        if extras:
            output['additional_info'] = extras

    ben_div = soup.find('div', id='jobOverview-7')
    if ben_div:
        benefits: dict = {}
        for h4 in ben_div.find_all('h4'):
            cat = _text(h4)
            ul = h4.find_next_sibling('ul')
            items = _list_items(ul)
            if items:
                benefits[cat] = items
        if benefits:
            output['benefits'] = benefits

    return output


def process_directory(input_dir: Path, base_dir: str, year: int, month: int, day: int, candidate: str = 'candidate') -> int:
    html_files = sorted(input_dir.glob('*.html'))
    if not html_files:
        _logger.error('No HTML files found in %s', input_dir)
        return 1

    success = 0
    for html_file in html_files:
        try:
            import secrets
            job_data = extract_job_posting(html_file)
            title = job_data.get('job_title', '') or html_file.stem
            location = job_data.get('location', '')
            city = location.split(',')[0].strip() if location else ''
            slug_source = f'{title} {city}'.strip() if city else title
            slug = slugify(slug_source) or slugify(html_file.stem)
            uid = secrets.token_hex(3)
            employer = job_data.get('employer', '')
            emp_short = employer_short_slug(employer)
            job_data['_uid'] = uid
            job_data['_slug'] = slug
            out_path = Path(job_details_json_path(base_dir, year, month, day, slug, emp_short, candidate, uid))
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'w') as f:
                json.dump(job_data, f, indent=2)
            _logger.info('Extracted: %s → %s', html_file.name, out_path)
            success += 1
        except Exception as exc:
            _logger.error('Failed to parse %s: %s', html_file, exc)

    return 0 if success == len(html_files) else 1


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Extract HTML job postings to JSON')
    parser.add_argument('input_dir', help='Path to {year}/{month}/{day}/ directory')
    args = parser.parse_args(argv)

    input_dir = Path(args.input_dir).resolve()
    if not input_dir.is_dir():
        _logger.error('input_dir does not exist: %s', input_dir)
        return 1

    parts = input_dir.parts
    try:
        year, month, day = int(parts[-3]), int(parts[-2]), int(parts[-1])
    except (ValueError, IndexError):
        _logger.error(
            'Cannot derive year/month/day from path: %s (expected .../YYYY/MM/DD)', input_dir
        )
        return 1

    cfg = load_config()
    set_level(cfg.get('log_level', 'info'))
    candidate = cfg.get('candidate_name', 'candidate')

    return process_directory(input_dir, cfg['job-listings_dir'], year, month, day, candidate)


if __name__ == '__main__':
    sys.exit(main())
