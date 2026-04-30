#!/usr/bin/env python3
"""
Orchestration script: correlation JSON → PDF generation (moved to orchestration/)

This mirrors the previous orchestration script but resolves helper scripts
relative to the new layout.
"""

import json
import os
import subprocess
import sys
import argparse
from pathlib import Path

# Ensure we can import utilities from the sibling utilities/ folder
SCRIPT_DIR = Path(__file__).parent
SYS_UTILS = str(SCRIPT_DIR.parent / 'utilities')
if SYS_UTILS not in sys.path:
    sys.path.insert(0, SYS_UTILS)

try:
    import naming_utils
except Exception:
    naming_utils = None


def run_command(command, check=True, capture_output=True):
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e}")
        if capture_output:
            print(f"Stderr: {e.stderr}")
        return None


def load_correlation(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading correlation file {path}: {e}")
        return None


def get_template_from_adapter(correlation_file):
    # adapter now lives in ../template_management/
    adapter_script = str((SCRIPT_DIR.parent / 'template_management' / 'py_adapter_correlator_to_template.py').resolve())
    if not os.path.exists(adapter_script):
        print(f"Error: Adapter script not found at {adapter_script}")
        return None

    result = run_command(f"python {adapter_script} {correlation_file}")
    if result is None or result.returncode != 0:
        return None

    try:
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error parsing adapter output: {e}")
        return None


def merge_template_data(unique_data_path, template_data):
    try:
        with open(unique_data_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading unique data: {e}")
        return False

    if template_data:
        data.update(template_data)

    try:
        with open(unique_data_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error writing unique data: {e}")
        return False


def run_preprocess_resume():
    preprocess_script = str((SCRIPT_DIR / "preprocess-resume.js").resolve())
    if not os.path.exists(preprocess_script):
        print(f"Error: preprocess-resume.js not found at {preprocess_script}")
        return False
    result = run_command(f"node {preprocess_script}")
    return result is not None and result.returncode == 0


def generate_pdf(correlation_file, candidate_name, template, dry_run=False):
    basename = Path(correlation_file).stem
    correlation_data = load_correlation(correlation_file)
    job_title = correlation_data.get('metadata', {}).get('job_title', '')

    # Prefer using naming_utils when available
    company_file = ''
    title_file = ''
    if naming_utils:
        # If correlator included job_json path, try to derive
        job_json_path = correlation_data.get('metadata', {}).get('job_json')
        base = naming_utils.derive_basename_from_job_json(job_json_path) if job_json_path else ''
        if base:
            company_file = base
            title_file = base
        else:
            # Fallback to sanitize job_title
            company_file = naming_utils.sanitize_for_filename(job_title)
            title_file = naming_utils.sanitize_for_filename(job_title)
    else:
        company_file = basename.replace('correlation_', '').replace('_', '-')
        title_file = job_title.replace(' ', '-').replace('/', '-').lower()

    artifacts_dir = Path('artifacts')
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # Build dated subdir
    dest_dir = naming_utils.build_dated_artifact_path(artifacts_dir, f"resume-{candidate_name}-{company_file}-{title_file}.pdf") if naming_utils else artifacts_dir / f"resume-{candidate_name}-{company_file}-{title_file}.pdf"

    pdf_name = str(dest_dir)

    if dry_run:
        print(f"[DRY RUN] Would generate: {pdf_name}")
        return True

    print(f"Generating PDF: {pdf_name}")

    # Ensure resume.json path is absolute
    resume_json = Path('resume.json').resolve()
    result = run_command(f"resumed export {resume_json} -t {template} -o {pdf_name}")
    if result is None or result.returncode != 0:
        print(f"Error generating PDF: {result.stderr if result else 'Unknown error'}")
        return False

    print(f"✓ Generated: {pdf_name}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Orchestrate correlation to PDF generation")
    parser.add_argument("correlation_file", help="Path to correlation JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Preview steps without generating PDF")
    parser.add_argument("--name", help="Candidate name")
    parser.add_argument("--template", help="PDF template")

    args = parser.parse_args()

    if not os.path.exists(args.correlation_file):
        print(f"Error: Correlation file not found: {args.correlation_file}")
        sys.exit(1)

    candidate_name = args.name or os.environ.get('RESUME_NAME', 'James Valeil')
    template = args.template or os.environ.get('RESUME_THEME', 'valeii-professional')

    print(f"Processing correlation: {args.correlation_file}")
    print(f"Candidate name: {candidate_name}")
    print(f"Template: {template}")
    print(f"Dry run: {args.dry_run}")

    print("\n1. Running adapter to infer domain and template data...")
    template_data = get_template_from_adapter(args.correlation_file)

    if not template_data:
        print("Warning: Adapter failed to provide template data. Using default template.")
        template_data = {
            'domain_inference': 'default',
            'job_title': 'unknown'
        }

    print(f"Adapter inference: {template_data.get('domain_inference', 'unknown')}")

    print("\n2. Merging template data into resume.unique-data.json...")
    unique_data_path = Path('resume.unique-data.json')

    if not unique_data_path.exists():
        print(f"Error: Unique data file not found: {unique_data_path}")
        sys.exit(1)

    if not merge_template_data(str(unique_data_path), template_data):
        print("Error: Failed to merge template data")
        sys.exit(1)

    print("✓ Template data merged successfully")

    print("\n3. Running preprocess-resume.js...")
    if not run_preprocess_resume():
        print("Error: Failed to run preprocess-resume.js")
        sys.exit(1)

    print("✓ Preprocessing completed successfully")

    print("\n4. Generating PDF...")
    if not generate_pdf(args.correlation_file, candidate_name, template, args.dry_run):
        print("Error: Failed to generate PDF")
        sys.exit(1)

    print("\n✓ PDF generation completed successfully")


if __name__ == "__main__":
    main()
