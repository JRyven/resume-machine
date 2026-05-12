from __future__ import annotations

import re
import secrets
import unicodedata
from pathlib import Path
from typing import Optional
import sys


_DROP_PHRASES = re.compile(
    r'\bgovernment\s+du\s+gourvernment\s+canada\b',
    re.IGNORECASE,
)

_DROP_WORDS = re.compile(
    r'\b(a|an|the|of|with|for)\b',
    re.IGNORECASE,
)

_ABBREVIATIONS: dict[str, str] = {
    'government': 'gov',
    'canada': 'ca',
    'developer': 'dev',
}


def _apply_abbreviations(s: str) -> str:
    def _replace(m: re.Match) -> str:
        return _ABBREVIATIONS.get(m.group(0).lower(), m.group(0))
    return re.sub(r'\b(' + '|'.join(re.escape(k) for k in _ABBREVIATIONS) + r')\b', _replace, s, flags=re.IGNORECASE)


def sanitize_for_filename(s: str) -> str:
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = _DROP_PHRASES.sub(' ', s)
    s = _DROP_WORDS.sub(' ', s)
    s = _apply_abbreviations(s)
    s = re.sub(r"[^0-9A-Za-z]+", '-', s)
    s = re.sub(r'-{2,}', '-', s)
    return s.strip('-').lower()[:200]


slugify = sanitize_for_filename


def job_json_path(base_dir: str, year: int, month: int, day: int, slug: str) -> str:
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/{slug}.json'


def employer_short_slug(employer: str) -> str:
    """Slugify only the first segment of a bilingual employer name (split on '/')."""
    first_part = employer.split('/')[0].strip()
    return slugify(first_part) or slugify(employer)


def job_details_json_path(
    base_dir: str, year: int, month: int, day: int,
    job_slug: str, employer_short: str, candidate: str, uid: str
) -> str:
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/{job_slug}_job-details_{employer_short}_{candidate}_{uid}.json'


def correlation_json_path(
    base_dir: str, year: int, month: int, day: int,
    job_slug: str, employer_short: str, candidate: str, uid: str
) -> str:
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/{job_slug}_resume_{employer_short}_{candidate}_{uid}.json'


def cover_letter_json_path(
    base_dir: str, year: int, month: int, day: int,
    job_slug: str, employer_short: str, candidate: str, uid: str
) -> str:
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/{job_slug}_letter_{employer_short}_{candidate}_{uid}.json'


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args:
        print('')
        sys.exit(0)
    if args[0] == 'sanitize' and len(args) >= 2:
        print(slugify(' '.join(args[1:])))
        sys.exit(0)
    if len(args) >= 2:
        company = args[0] or ''
        title = args[1] or ''
        base = f"{company} {title}".strip()
        print(slugify(base))
        sys.exit(0)
    print(slugify(args[0]))
