#!/usr/bin/env python3
"""Build resume PDF from YAML content using composition engine and `resumed`.

This script:
- loads `base` YAML and 0..n fragment YAML files
- composes them using `Composer`
- writes a JSON resume to a build path
- optionally calls the `resumed` CLI to render a PDF

Designed for testability: `main(argv)` callable from tests.
"""
import argparse
import datetime
import json
import os
import shlex
import subprocess
import sys

import yaml

_lib_dir = os.path.join(os.path.dirname(__file__), "_lib")
sys.path.insert(0, _lib_dir)

from composer import Composer
from validator import Validator


def _safe_slug(name: str) -> str:
    if not name:
        return "unknown"
    s = name.strip().lower()
    for ch in [" ", "_", ","]:
        s = s.replace(ch, "-")
    # reduce multiple dashes
    while "--" in s:
        s = s.replace("--", "-")
    return s


def _make_filename(resume_json: dict, role: str) -> str:
    name = resume_json.get("basics", {}).get("name") or resume_json.get("name") or "unknown"
    slug = _safe_slug(name)
    date = datetime.date.today().strftime("%Y%m%d")
    role_part = _safe_slug(role) if role else "role"
    return f"{slug}-{role_part}-{date}.pdf"


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main(argv=None):
    p = argparse.ArgumentParser(description="Build resume PDF from YAML fragments")
    p.add_argument("--base", required=True, help="Path to base YAML file")
    p.add_argument("--fragments", nargs="*", default=[], help="YAML fragment files to merge")
    p.add_argument("--role", help="Role key (used for filename and optionally to load a role fragment)")
    p.add_argument("--output-dir", default="artifacts", help="Directory to write PDF and artifacts")
    p.add_argument("--validate", help="Path to JSON Schema file to validate against")
    p.add_argument("--dry-run", action="store_true", help="Do everything except call `resumed`")
    p.add_argument("--verbose", action="store_true", help="Verbose logging")
    args = p.parse_args(argv)

    fragments = list(args.fragments or [])
    if args.role:
        # If a role fragment exists under content/roles/{role}.yaml, prefer that
        candidate = os.path.join("content", "roles", f"{args.role}.yaml")
        if os.path.exists(candidate):
            fragments.append(candidate)

    base = load_yaml(args.base)
    frag_objs = [load_yaml(p) for p in fragments]

    composer = Composer()
    merged = composer.merge(base, frag_objs)

    if args.validate:
        validator = Validator()
        validator.load_schema_from_file(args.validate)
        ok, err = validator.validate(merged)
        if not ok:
            print(f"Validation failed: {err}", file=sys.stderr)
            return 2

    os.makedirs(args.output_dir, exist_ok=True)
    build_json_path = os.path.join(args.output_dir, "resume.json")
    with open(build_json_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    pdf_name = _make_filename(merged, args.role or "role")
    pdf_path = os.path.join(args.output_dir, pdf_name)

    # store metadata sidecar (non-visible) to avoid visible timestamps
    metadata = {"generated_at": datetime.datetime.utcnow().isoformat() + "Z", "role": args.role}
    with open(os.path.join(args.output_dir, "resume.metadata.json"), "w", encoding="utf-8") as m:
        json.dump(metadata, m, indent=2)

    print(f"Wrote JSON resume to {build_json_path}")
    if args.dry_run:
        print("Dry-run: skipping PDF generation")
        print(f"PDF would be: {pdf_path}")
        return 0

    # Call `resumed` CLI to render PDF. If not found, print helpful message.
    try:
        cmd = ["resumed", build_json_path, "-o", pdf_path]
        if args.verbose:
            print("Running:", shlex.join(cmd))
        subprocess.run(cmd, check=True)
        print(f"Wrote PDF to {pdf_path}")
        return 0
    except FileNotFoundError:
        print("`resumed` not found in PATH. Install resumed or run with --dry-run.", file=sys.stderr)
        return 3
    except subprocess.CalledProcessError as e:
        print(f"resumed failed: {e}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
