#!/usr/bin/env python3
"""Compose YAML fragments into a JSON Resume document.

Usage: python compose_resume.py --base content/base.yaml --fragments content/fragments/role.yaml -o build/resume.json --validate
"""
import argparse
import json
import os
import sys

import yaml

_lib_dir = os.path.join(os.path.dirname(__file__), "_lib")
sys.path.insert(0, _lib_dir)

from composer import Composer
from validator import Validator


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main(argv=None):
    p = argparse.ArgumentParser(description="Compose YAML fragments into a JSON Resume")
    p.add_argument("--base", required=True, help="Base YAML file")
    p.add_argument("--fragments", nargs="*", help="Fragment YAML files to merge", default=[])
    p.add_argument("-o", "--output", required=True, help="Output JSON file path")
    p.add_argument("--validate", help="Path to JSON Schema file to validate against", default=None)
    args = p.parse_args(argv)

    base = load_yaml(args.base)
    fragments = [load_yaml(p) for p in args.fragments]

    composer = Composer()
    merged = composer.merge(base, fragments)

    if args.validate:
        validator = Validator()
        validator.load_schema_from_file(args.validate)
        ok, err = validator.validate(merged)
        if not ok:
            print(f"Validation failed: {err}", file=sys.stderr)
            return 2

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as out:
        json.dump(merged, out, indent=2, ensure_ascii=False)

    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
