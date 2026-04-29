#!/usr/bin/env python3
"""
Orchestration script: correlation JSON → PDF generation.

This script takes a correlation_*.json file and generates a PDF resume
using the resume-machine workflow, including:
1. Running adapter to infer domain + template data
2. Merging template data into resume.unique-data.json
3. Running preprocess-resume.js to produce resume.json
4. Exporting PDF via resumed CLI

Usage:
  python py_orchestrate_correlation_to_pdf.py <correlation_json_path> [options]

Options:
  --dry-run          Preview steps without generating PDF
  --name NAME        Candidate name (default: "James Valeil")
  --template TEMPLATE  PDF template (default: "valeii-professional")
  --help             Show this help message
"""

import json
import os
import subprocess
import sys
import argparse
from pathlib import Path

def run_command(command, check=True, capture_output=True):
    """Run a shell command and return result."""
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
    """Load correlation JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading correlation file {path}: {e}")
        return None

def get_template_from_adapter(correlation_file):
    """Run adapter to get template data from correlation."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    adapter_script = os.path.join(script_dir, "py_adapter_correlator_to_template.py")
    
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
    """Merge template data into resume.unique-data.json."""
    try:
        with open(unique_data_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading unique data: {e}")
        return False
    
    # Merge adapter template data
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
    """Run preprocess-resume.js to generate resume.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    preprocess_script = os.path.join(script_dir, "preprocess-resume.js")
    
    if not os.path.exists(preprocess_script):
        print(f"Error: preprocess-resume.js not found at {preprocess_script}")
        return False
    
    result = run_command(f"node {preprocess_script}")
    return result is not None and result.returncode == 0

def generate_pdf(correlation_file, candidate_name, template, dry_run=False):
    """Generate PDF using resumed CLI."""
    # Get the basename from the correlation file for naming
    basename = Path(correlation_file).stem  # e.g., correlation_software_developer_kanata
    
    # Extract job title from correlation metadata
    correlation_data = load_correlation(correlation_file)
    job_title = correlation_data.get('metadata', {}).get('job_title', 'unknown')
    
    # Sanitize job title for filename
    company_file = basename.replace('correlation_', '').replace('_', '-')
    title_file = job_title.replace(' ', '-').replace('/', '-').lower()
    
    pdf_name = f"resume-machine/artifacts/resume-{candidate_name}-{company_file}-{title_file}.pdf"
    
    if dry_run:
        print(f"[DRY RUN] Would generate: {pdf_name}")
        return True
    
    print(f"Generating PDF: {pdf_name}")
    
    # Run resumed export
    result = run_command(f"resumed export resume.json -t {template} -o {pdf_name}")
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
    
    # Validate correlation file
    if not os.path.exists(args.correlation_file):
        print(f"Error: Correlation file not found: {args.correlation_file}")
        sys.exit(1)
    
    # Get environment variables as fallbacks
    candidate_name = args.name or os.environ.get('RESUME_NAME', 'James Valeil')
    template = args.template or os.environ.get('RESUME_THEME', 'valeii-professional')
    
    print(f"Processing correlation: {args.correlation_file}")
    print(f"Candidate name: {candidate_name}")
    print(f"Template: {template}")
    print(f"Dry run: {args.dry_run}")
    
    # Step 1: Run adapter to get template data
    print("\n1. Running adapter to infer domain and template data...")
    template_data = get_template_from_adapter(args.correlation_file)
    
    if not template_data:
        print("Warning: Adapter failed to provide template data. Using default template.")
        # Create minimal template data for default case
        template_data = {
            'domain_inference': 'default',
            'job_title': 'unknown'
        }
    
    print(f"Adapter inference: {template_data.get('domain_inference', 'unknown')}")
    
    # Step 2: Merge template data into resume.unique-data.json
    print("\n2. Merging template data into resume.unique-data.json...")
    unique_data_path = "resume.unique-data.json"
    
    if not os.path.exists(unique_data_path):
        print(f"Error: Unique data file not found: {unique_data_path}")
        sys.exit(1)
    
    if not merge_template_data(unique_data_path, template_data):
        print("Error: Failed to merge template data")
        sys.exit(1)
    
    print("✓ Template data merged successfully")
    
    # Step 3: Run preprocess-resume.js
    print("\n3. Running preprocess-resume.js...")
    if not run_preprocess_resume():
        print("Error: Failed to run preprocess-resume.js")
        sys.exit(1)
    
    print("✓ Preprocessing completed successfully")
    
    # Step 4: Generate PDF
    print("\n4. Generating PDF...")
    if not generate_pdf(args.correlation_file, candidate_name, template, args.dry_run):
        print("Error: Failed to generate PDF")
        sys.exit(1)
    
    print("\n✓ PDF generation completed successfully")

if __name__ == "__main__":
    main()
