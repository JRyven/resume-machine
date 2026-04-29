from __future__ import annotations

import re
import unicodedata
from pathlib import Path
from datetime import date
from typing import Optional


def sanitize_for_filename(s: str) -> str:
    if not s:
        return ''
    # Normalize and remove accents
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    # Lowercase, replace non-alphanum with dash
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
