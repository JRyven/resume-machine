#!/usr/bin/env python3
"""
End-to-end orchestrator: correlation JSON → PDF.

Steps:
  1. Run adapter  → infer domain + template data
  2. Merge template into resume.unique-data.json
  3. Run preprocess-resume.js → produce resume.json
  4. Export PDF via `resumed` CLI

Usage:
  python py_orchestrate_correlation_to_pdf.py <correlation_json_path> [options]

Options:
  --dry-run          Preview steps without writing files or running commands.
  --name=<name>      Candidate name used in the PDF filename  (default: read from env RESUME_NAME).
  --template=<name>  resumed theme/template name              (default: read from env RESUME_THEME).

Environment variables (fallback when flags are omitted):
  RESUME_NAME   — candidate name for PDF filename (e.g. "Jane-Smith")
  RESUME_THEME  — resumed theme slug              (e.g. "my-professional")
  RESUME_CONFIG_FILE — path to YAML config file (default: resume-machine/config.yaml)
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional
from datetime import date

# Add config manager import
sys.path.append(str(Path(__file__).parent))
try:
    from config_manager import load_config
except ImportError:
    # Fallback if config_manager is not available
    def load_config(config_file=None):
        return {}

try:
    from naming_utils import derive_basename_from_job_json, build_dated_artifact_path, sanitize_for_filename
except ImportError:
    def derive_basename_from_job_json(x):
        return ''
    def build_dated_artifact_path(artifacts_dir, base_name):
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        return artifacts_dir / base_name
    def sanitize_for_filename(s):
        return s.replace(' ', '-') if s else ''


# ════════════════════════════════════════════════════════════════════════════════
# CONFIG (resolved relative to this script)
# ════════════════════════════════════════════════════════════════════════════════

_SCRIPT_DIR     = Path(__file__).parent
_PROJECT_ROOT   = _SCRIPT_DIR.parents[1]

ADAPTER_SCRIPT      = _SCRIPT_DIR / 'py_adapter_correlator_to_template.py'
PREPROCESS_SCRIPT   = _SCRIPT_DIR / 'preprocess-resume.js'
UNIQUE_DATA_DEST    = _SCRIPT_DIR.parent / 'role-based-templates' / 'default' / 'resume.unique-data.json'
ARTIFACTS_DIR       = _SCRIPT_DIR.parent / 'artifacts'


# ════════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════════

def _run(cmd: list[str], desc: str) -> str:
    """
    Run a subprocess, printing a header and streaming stdout.
    Exits with code 1 on failure.

    Returns:
        Captured stdout as a string.
    """
    print(f'\n{"="*70}\n>> {desc}\n{"="*70}')
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f'ERROR: {desc} failed\n{result.stderr}', file=sys.stderr)
        sys.exit(1)
    return result.stdout


def _parse_args(argv: list[str]) -> dict:
    """Parse CLI flags into a config dict."""
    config = {
        'correlation_path': None,
        'dry_run':          '--dry-run' in argv,
        'name':             None,
        'theme':            None,
    }
    for arg in argv[1:]:
        if arg.startswith('--name='):
            config['name'] = arg.split('=', 1)[1]
        elif arg.startswith('--template='):
            config['theme'] = arg.split('=', 1)[1]
        elif not arg.startswith('--'):
            config['correlation_path'] = arg
    return config


def _resolve_candidate_name(config: dict, app_config: dict) -> str:
    name = config.get('name') or os.environ.get('RESUME_NAME', '')
    if not name and 'candidate_name' in app_config:
        name = app_config['candidate_name']
    if not name:
        raise ValueError(
            'Candidate name is required. Pass --name=<name>, set RESUME_NAME, or configure in config.yaml'
        )
    return name


def _resolve_theme(config: dict, app_config: dict) -> str:
    theme = config.get('theme') or os.environ.get('RESUME_THEME', '')
    if not theme and 'theme' in app_config:
        theme = app_config['theme']
    if not theme:
        raise ValueError(
            'Resume theme is required. Pass --template=<theme>, set RESUME_THEME, or configure in config.yaml'
        )
    return theme


# ════════════════════════════════════════════════════════════════════════════════
# PIPELINE STEPS
# ════════════════════════════════════════════════════════════════════════════════

def step_run_adapter(correlation_path: Path, dry_run: bool) -> dict:
    """Step 1 — Run adapter and parse the resulting template dict."""
    cmd = ['python', str(ADAPTER_SCRIPT), str(correlation_path)]

    if dry_run:
        print(f'[DRY RUN] Step 1: Run adapter\n  Command: {" ".join(cmd)}')
        # Still run the adapter in dry-run so we can show what would be merged.
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            print('  (adapter unavailable — skipping preview)', file=sys.stderr)
            return {}
        output = result.stdout
    else:
        output = _run(cmd, 'Step 1: Run adapter (correlation → template)')

    try:
        template = json.loads(output)
    except json.JSONDecodeError as e:
        print(f'ERROR: Adapter output is not valid JSON: {e}', file=sys.stderr)
        sys.exit(1)

    print(
        f'  Domain   : {template.get("domain_inference", "n/a")}\n'
        f'  Languages: {template.get("featured_languages", "n/a")}\n'
        f'  Job      : {template.get("job_title", "n/a")}'
    )
    return template


def step_merge_template(template: dict, dry_run: bool) -> None:
    """Step 2 — Merge template into resume.unique-data.json."""
    if dry_run:
        print(f'[DRY RUN] Step 2: Merge template → {UNIQUE_DATA_DEST}')
        return

    existing: dict = {}
    if UNIQUE_DATA_DEST.exists():
        with open(UNIQUE_DATA_DEST) as f:
            existing = json.load(f)

    UNIQUE_DATA_DEST.parent.mkdir(parents=True, exist_ok=True)
    with open(UNIQUE_DATA_DEST, 'w') as f:
        json.dump({**existing, **template}, f, indent=2)

    print(f'✓ Merged template into {UNIQUE_DATA_DEST}')


def step_preprocess(dry_run: bool) -> None:
    """Step 3 — Run preprocess-resume.js (variable substitution → resume.json)."""
    cmd = ['node', str(PREPROCESS_SCRIPT)]
    if dry_run:
        print(f'[DRY RUN] Step 3: Preprocess resume\n  Command: {" ".join(cmd)}')
    else:
        _run(cmd, 'Step 3: Preprocess resume (variable substitution)')


def step_export_pdf(template: dict, candidate_name: str, theme: str, dry_run: bool, correlation_path: Path) -> None:
    """Step 4 — Export resume.json to PDF via the `resumed` CLI.

    This step attempts to build a friendly filename. Priority:
      1. Use `job_title` from the template
      2. Fallback to the referenced job JSON filename recorded in the correlation file
      3. Use a sanitized placeholder
    The PDF is written into a dated artifacts subdirectory (YYYY/MM/DD).
    """

    # Prefer explicit job_title from the merged template
    raw_job = template.get('job_title') or ''
    # If missing, try to read the correlation file to find the original job JSON path
    if not raw_job:
        try:
            with open(correlation_path) as f:
                corr = json.load(f)
            job_json_ref = corr.get('metadata', {}).get('job_json') or corr.get('metadata', {}).get('job_json_path')
        except Exception:
            job_json_ref = None
        basename = derive_basename_from_job_json(job_json_ref)
        raw_job = basename or 'job'

    job_slug = sanitize_for_filename(raw_job)
    pdf_name = f'resume-{sanitize_for_filename(candidate_name)}-{job_slug}.pdf'

    # Put into dated artifacts directory to match batch behavior
    pdf_path = build_dated_artifact_path(ARTIFACTS_DIR, pdf_name)

    resume_json_path = _PROJECT_ROOT / 'resume.json'
    cmd = ['resumed', 'export', str(resume_json_path), '-t', theme, '-o', str(pdf_path)]
    if dry_run:
        print(f'[DRY RUN] Step 4: Export PDF\n  Command: {" ".join(cmd)}')
    else:
        _run(cmd, f'Step 4: Export PDF → {pdf_path}')


# ════════════════════════════════════════════════════════════════════════════════
# ORCHESTRATION ENTRY POINT
# ════════════════════════════════════════════════════════════════════════════════

def orchestrate(correlation_path: str, dry_run: bool, candidate_name: str, theme: str) -> None:
    path = Path(correlation_path).resolve()
    if not path.exists():
        print(f'ERROR: Correlation file not found: {path}', file=sys.stderr)
        sys.exit(1)

    print(f'\n{"#"*70}')
    print('# Orchestration: Correlation → Template → Resume → PDF')
    print(f'{"#"*70}')
    print(f'Correlation: {path}')
    print(f'Dry run    : {dry_run}')

    template = step_run_adapter(path, dry_run)
    step_merge_template(template, dry_run)
    step_preprocess(dry_run)
    step_export_pdf(template, candidate_name, theme, dry_run, path)

    print(f'\n{"#"*70}\n# ✓ Pipeline complete!\n{"#"*70}')


# ════════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════════

def main() -> None:
    # Load configuration
    config = _parse_args(sys.argv)
    
    # Get config file path from environment or use default
    config_file = os.environ.get('RESUME_CONFIG_FILE') or 'resume-machine/config.yaml'
    
    # Load config from file and environment
    app_config = load_config(config_file)
    
    if not config['correlation_path']:
        print(
            'Usage: python py_orchestrate_correlation_to_pdf.py <correlation_json_path> '
            '[--dry-run] [--name=<name>] [--template=<theme>]',
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        # Resolve candidate name (CLI flag > env var > config > default)
        candidate_name = _resolve_candidate_name(config, app_config)
        if not candidate_name:
            raise ValueError(
                'Candidate name is required. Pass --name=<name>, set RESUME_NAME, or configure in config.yaml'
            )
            
        # Resolve theme (CLI flag > env var > config > default)
        theme = _resolve_theme(config, app_config)
        if not theme:
            raise ValueError(
                'Resume theme is required. Pass --template=<theme>, set RESUME_THEME, or configure in config.yaml'
            )
    except ValueError as e:
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)

    orchestrate(
        correlation_path=config['correlation_path'],
        dry_run=config['dry_run'],
        candidate_name=candidate_name,
        theme=theme,
    )


if __name__ == '__main__':
    main()
