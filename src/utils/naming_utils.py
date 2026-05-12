from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from typing import Optional
import sys


def sanitize_for_filename(s: str) -> str:
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r"[^0-9A-Za-z]+", '-', s)
    s = re.sub(r'-{2,}', '-', s)
    return s.strip('-').lower()[:200]


slugify = sanitize_for_filename


def job_json_path(base_dir: str, year: int, month: int, day: int, slug: str) -> str:
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/{slug}.json'


def correlation_json_path(
    base_dir: str, year: int, month: int, day: int,
    candidate: str, employer: str, title: str
) -> str:
    employer_slug = slugify(employer)
    title_slug = slugify(title)
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/resume-{candidate}-{employer_slug}-{title_slug}.json'


def cover_letter_json_path(
    base_dir: str, year: int, month: int, day: int,
    candidate: str, employer: str, title: str
) -> str:
    employer_slug = slugify(employer)
    title_slug = slugify(title)
    return f'{base_dir}/{year}/{month:02d}/{day:02d}/letter-{candidate}-{employer_slug}-{title_slug}.json'


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
