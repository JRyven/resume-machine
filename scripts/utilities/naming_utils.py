from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from datetime import date
from typing import Optional
import sys


def sanitize_for_filename(s: str) -> str:
    if not s:
        return ''
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = re.sub(r"[^0-9A-Za-z]+", '-', s)
    s = re.sub(r'-{2,}', '-', s)
    return s.strip('-')[:200]


def build_dated_artifact_path(artifacts_dir: Path, base_name: str) -> Path:
    today = date.today()
    dest = artifacts_dir / f"{today.year}" / f"{today.month:02d}" / f"{today.day:02d}"
    dest.mkdir(parents=True, exist_ok=True)
    return dest / base_name


def derive_basename_from_job_json(job_json_path: Optional[str]) -> str:
    if not job_json_path:
        return ''
    p = Path(job_json_path)
    name = p.stem
    return sanitize_for_filename(name)


if __name__ == '__main__':
    # CLI compatibility for existing shell scripts: two modes
    # 1) `naming_utils.py <company> <title>` -> prints combined sanitized basename
    # 2) `naming_utils.py sanitize "Some String"` -> prints sanitized string
    args = sys.argv[1:]
    if not args:
        print('')
        sys.exit(0)

    if args[0] == 'sanitize' and len(args) >= 2:
        print(sanitize_for_filename(' '.join(args[1:])))
        sys.exit(0)

    # Default: company + title
    if len(args) >= 2:
        company = args[0] or ''
        title = args[1] or ''
        base = f"{company} {title}".strip()
        print(sanitize_for_filename(base))
        sys.exit(0)

    # Fallback: sanitize single argument
    print(sanitize_for_filename(args[0]))
