#!/usr/bin/env python3
"""
Orchestration example: End-to-end workflow using the adapter.

This shows how correlation data flows through the adapter into artifact generation.

Usage:
  python py_orchestrate_correlation_to_pdf.py <correlation_json_path> [--dry-run]
  
Example:
  python py_orchestrate_correlation_to_pdf.py \\
    jobbankjobs/2026/04/05/correlation_software_developer_kanata.json
    
Steps:
  1. Load correlation data
  2. Run adapter → extract template
  3. Merge template into resume.unique-data.json
  4. Run preprocess-resume.js → generate resume.json
  5. Export resume as PDF (using `resumed` CLI)
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def run_command(cmd: list, desc: str = "", dry_run: bool = False) -> Optional[str]:
    """Execute shell command; return stdout on success, exit on failure."""
    if dry_run:
        print(f"[DRY RUN] {desc}")
        print(f"  Command: {' '.join(cmd)}")
        return None
    
    print(f"\n{'='*70}")
    print(f"{'>'*2} {desc}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {desc} failed", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(1)


def orchestrate(correlation_path: str, dry_run: bool = False):
    """
    Full pipeline: correlation → template → resume.json → PDF
    """
    correlation_path = Path(correlation_path).resolve()
    if not correlation_path.exists():
        print(f"ERROR: Correlation file not found: {correlation_path}", file=sys.stderr)
        sys.exit(1)
    
    # Infer paths from correlation location
    project_root = Path.cwd()
    adapter_script = project_root / 'resume-machine/scripts/py_adapter_correlator_to_template.py'
    preprocess_script = project_root / 'resume-machine/scripts/preprocess-resume.js'
    unique_data_dest = project_root / 'resume-machine/role-based-templates/default/resume.unique-data.json'
    
    print(f"\n{'#'*70}")
    print(f"# Orchestration: Correlation → Template → Resume → PDF")
    print(f"{'#'*70}")
    print(f"Project root: {project_root}")
    print(f"Correlation:  {correlation_path}")
    print(f"Dry run:      {dry_run}")
    
    # Step 1: Run adapter
    adapter_output = run_command(
        ['python', str(adapter_script), str(correlation_path)],
        "Step 1: Run adapter (correlation → template)",
        dry_run
    )
    
    # For dry-run, still load template from correlation to show what would happen
    template_data = {}
    if dry_run:
        try:
            result = subprocess.run(
                ['python', str(adapter_script), str(correlation_path)],
                capture_output=True, text=True, check=True
            )
            adapter_output = result.stdout
        except:
            pass
    
    if not adapter_output:
        print("ERROR: Adapter produced no output", file=sys.stderr)
        sys.exit(1)
    
    try:
        template_data = json.loads(adapter_output)
        print(f"\n✓ Template generated successfully")
        print(f"  Domain:    {template_data.get('domain_inference', 'N/A')}")
        print(f"  Languages: {template_data.get('featured_languages', 'N/A')}")
        print(f"  Job:       {template_data.get('job_title', 'N/A')}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Adapter output is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Step 2: Merge template into resume.unique-data.json
    if not dry_run and adapter_output:
        print(f"\n{'='*70}")
        print(f"{'>'*2} Step 2: Merge template into resume.unique-data.json")
        print(f"{'='*70}")
        
        # Read existing data
        existing_data = {}
        if unique_data_dest.exists():
            with open(unique_data_dest, 'r') as f:
                existing_data = json.load(f)
        
        # Merge template
        merged_data = {**existing_data, **template_data}
        
        # Write back
        unique_data_dest.parent.mkdir(parents=True, exist_ok=True)
        with open(unique_data_dest, 'w') as f:
            json.dump(merged_data, f, indent=2)
        
        print(f"✓ Merged template into {unique_data_dest}")
    
    # Step 3: Run preprocess-resume.js
    run_command(
        ['node', str(preprocess_script)],
        "Step 3: Preprocess resume (variable substitution)",
        dry_run
    )
    
    # Step 4: Export resume as PDF
    pdf_name = f"resume-James-Valeii-{template_data.get('job_title', 'job').replace(' ', '-')}.pdf"
    run_command(
        ['resumed', 'export', 'resume.json', '-t', 'valeii-professional', '-o', f'artifacts/{pdf_name}'],
        f"Step 4: Export PDF → artifacts/{pdf_name}",
        dry_run
    )
    
    print(f"\n{'#'*70}")
    print(f"# ✓ Pipeline complete!")
    print(f"{'#'*70}")


def main():
    if len(sys.argv) < 2:
        print(
            "Usage: python py_orchestrate_correlation_to_pdf.py <correlation_json_path> [--dry-run]\n",
            file=sys.stderr
        )
        sys.exit(1)
    
    correlation_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv
    
    orchestrate(correlation_path, dry_run)


if __name__ == '__main__':
    main()
