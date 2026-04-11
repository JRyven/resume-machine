#!/usr/bin/env python3
"""
USAGE EXAMPLES: Modular Job Skill Analyzer Pipeline

This file demonstrates how to use individual pipeline stages
independently or in combination.
"""

from job_skill_analyzer import (
    load_skills_index,
    extract_skills_from_posting,
    resolve_facet,
    match_posting_to_skills,
    print_report,
    save_match_report,
    analyze_job_posting,
    batch_analyze_job_postings,
    ALIASES,
)


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 1: Load and inspect skills index
# ════════════════════════════════════════════════════════════════════════════════

def example_inspect_index():
    """Load skills index and see what we have"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Inspect Skills Index")
    print("="*80)
    
    index = load_skills_index()
    
    print(f"\nLoaded {len(index['facet_by_name'])} facets:")
    for facet_name, entry in sorted(index['facet_by_name'].items())[:10]:
        print(f"  • {facet_name:30} → {entry['facet_type']}")
    print(f"  ... and {len(index['facet_by_name']) - 10} more\n")
    
    print(f"Alias table has {len(ALIASES)} entries:")
    for key, val in sorted(list(ALIASES.items())[:5]):
        print(f"  • '{key}' → {val}")
    print(f"  ... and {len(ALIASES) - 5} more\n")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 2: Extract skills from a single posting
# ════════════════════════════════════════════════════════════════════════════════

def example_extract_single_posting():
    """Extract skills from one job posting"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Extract Skills from Single Posting")
    print("="*80)
    
    html_file = 'jobbankjobs/2026/04/05/software developer - Kanata, ON - Job posting - Job Bank.html'
    
    sections = extract_skills_from_posting(html_file)
    
    print(f"\nExtracted {len(sections)} sections from {html_file}:")
    for section_label, items in sections.items():
        print(f"\n  [{section_label}] — {len(items)} items")
        for item in items[:3]:
            print(f"    • {item}")
        if len(items) > 3:
            print(f"    ... and {len(items) - 3} more")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 3: Test skill resolution individually
# ════════════════════════════════════════════════════════════════════════════════

def example_resolve_individual_skills():
    """Test how raw skills are mapped to facets"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Test Skill Resolution")
    print("="*80)
    
    index = load_skills_index()
    
    test_skills = [
        'React',          # Should match exactly
        'spring boot',    # Should match via alias (Spring Framework)
        'kubernetes',     # Should match via alias (Kubernetes)
        'foobar',         # No match
        'unix shell',     # Should match via substring
    ]
    
    print(f"\nTesting skill resolution against facet catalog:\n")
    for raw_skill in test_skills:
        result = resolve_facet(raw_skill, index)
        if result:
            print(f"  ✓ '{raw_skill}' → {result['facet_name']} ({result['facet_type']})")
        else:
            print(f"  ✗ '{raw_skill}' → NO MATCH")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 4: Full pipeline on a single job
# ════════════════════════════════════════════════════════════════════════════════

def example_full_pipeline_single_job():
    """Extract, match, and report on one job posting"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Full Pipeline (Extract → Match → Report)")
    print("="*80)
    
    html_file = 'jobbankjobs/2026/04/05/software developer - Kanata, ON - Job posting - Job Bank.html'
    
    # One-liner: full pipeline
    result = analyze_job_posting(html_file, verbose=True)
    
    print(f"\nReport saved to: {result['output_file']}")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 5: Custom report generation
# ════════════════════════════════════════════════════════════════════════════════

def example_custom_reporting():
    """Extract + match, then create custom report"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Custom Report Generation")
    print("="*80)
    
    index = load_skills_index()
    html_file = 'jobbankjobs/2026/04/05/application programmer - Kanata, ON - Job posting - Job Bank.html'
    
    # Extract and match
    sections = extract_skills_from_posting(html_file)
    report = match_posting_to_skills(sections, index)
    
    # Custom reporting
    s = report['summary']
    print(f"\nJob Analysis Summary:")
    print(f"  Total skills found: {s['total_skills_extracted']}")
    print(f"  Successfully matched: {s['matched_to_facets']} ({s['match_rate_pct']}%)")
    print(f"  Need new aliases for: {s['unmatched']}")
    
    print(f"\nMatched Skills:")
    for matched in report['matched']:
        if not matched['duplicate']:
            print(f"  • {matched['raw_skill']:<40} → {matched['facet_name']}")
    
    print(f"\nTop Unmatched Skills (gaps):")
    for unmatched in report['unmatched'][:5]:
        print(f"  • {unmatched['raw_skill']:<40} ({unmatched['source_section']})")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 6: Batch processing all jobs with filtering
# ════════════════════════════════════════════════════════════════════════════════

def example_batch_analysis_with_filtering():
    """Process all jobs and find high-match ones"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Batch Analysis with Filtering")
    print("="*80)
    
    results = batch_analyze_job_postings(verbose=False)
    
    # Filter to high-match jobs
    high_match_jobs = [
        r for r in results
        if r['success'] and r['result']['report']['summary']['match_rate_pct'] > 10
    ]
    
    print(f"\nJobs with >10% skill match:")
    for job in sorted(high_match_jobs, 
                      key=lambda x: x['result']['report']['summary']['match_rate_pct'],
                      reverse=True):
        match_rate = job['result']['report']['summary']['match_rate_pct']
        matched = job['result']['report']['summary']['matched_to_facets']
        total = job['result']['report']['summary']['total_skills_extracted']
        print(f"  • {job['file']:<60} {matched}/{total} ({match_rate}%)")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 7: Identify missing aliases
# ════════════════════════════════════════════════════════════════════════════════

def example_identify_missing_aliases():
    """Find common unmatched skills across all jobs"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Identify Missing Aliases (For ALIASES Table)")
    print("="*80)
    
    results = batch_analyze_job_postings(verbose=False)
    
    # Collect all unmatched skills
    unmatched_skills = {}
    for r in results:
        if r['success']:
            for unmatched in r['result']['report']['unmatched']:
                skill = unmatched['raw_skill']
                unmatched_skills[skill] = unmatched_skills.get(skill, 0) + 1
    
    # Show most common unmatched skills
    print(f"\nMost common unmatched skills (candidates for ALIASES):\n")
    sorted_skills = sorted(unmatched_skills.items(), key=lambda x: x[1], reverse=True)
    for skill, count in sorted_skills[:15]:
        print(f"  • {skill:<50} appears in {count} postings")
        print(f"    Consider adding to ALIASES table")


# ════════════════════════════════════════════════════════════════════════════════
# EXAMPLE 8: Programmatic access to all data
# ════════════════════════════════════════════════════════════════════════════════

def example_access_all_data():
    """Access full analysis data for downstream processing"""
    print("\n" + "="*80)
    print("EXAMPLE 8: Full Data Access (for ML/downstream)")
    print("="*80)
    
    index = load_skills_index()
    html_file = 'jobbankjobs/2026/04/05/full stack developer - Toronto, ON - Job posting - Job Bank.html'
    
    sections = extract_skills_from_posting(html_file)
    report = match_posting_to_skills(sections, index)
    
    # Access structured data
    print(f"\nAll matched facets:")
    for matched in report['matched']:
        if not matched['duplicate']:
            print(f"  {matched['facet_id']:30} {matched['facet_name']:30} {matched['facet_type']}")
    
    print(f"\nAll unmatched skills:")
    for unmatched in report['unmatched']:
        print(f"  {unmatched['raw_skill']:50} [{unmatched['source_section']}]")
    
    # Can be serialized to JSON, fed to ML model, etc.
    output_file = save_match_report(html_file, sections, report, 'full_analysis.json')
    print(f"\nFull data serialized to: {output_file}")


# ════════════════════════════════════════════════════════════════════════════════
# RUN ALL EXAMPLES
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    example_inspect_index()
    example_extract_single_posting()
    example_resolve_individual_skills()
    # example_full_pipeline_single_job()  # Uncomment for verbose output
    example_custom_reporting()
    example_batch_analysis_with_filtering()
    example_identify_missing_aliases()
    # example_access_all_data()  # Uncomment to see full data access
    
    print("\n" + "="*80)
    print("All examples completed.")
    print("="*80 + "\n")
