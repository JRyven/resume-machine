#!/usr/bin/env python3
"""
Modular job posting extraction + skills matching pipeline.

Pipeline stages (all individually accessible):
  1. load_skills_index() — Load and index facet_catalog
  2. extract_skills_from_posting() — Parse HTML → sections with skills
  3. resolve_facet() — Match raw skill string → facet entry
  4. match_posting_to_skills() — Generate match report
  5. print_report() — Pretty-print results
  6. save_match_report() — Persist to JSON

Usage (modular):
  >>> index = load_skills_index()
  >>> sections = extract_skills_from_posting('job.html')
  >>> report = match_posting_to_skills(sections, index)
  >>> print_report(report, sections)
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from bs4 import BeautifulSoup


# ════════════════════════════════════════════════════════════════════════════════
# CONFIG
# ════════════════════════════════════════════════════════════════════════════════

SKILLS_INDEX_PATH = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/resume-machine/skills-index.json'
JOB_HTML_DIR = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/04/05'

# Alias table: maps terms in job postings → canonical facet_name in skills index
# (Extend this as you encounter new postings)
ALIASES: Dict[str, str] = {
    # ── Languages ─────────────────────────────────────────────────────────────
    'c'                                    : 'C',
    'c++'                                  : 'C++',
    'c#'                                   : 'C#',
    'csharp'                               : 'C#',
    'java'                                 : 'Java',
    'javascript'                           : 'JavaScript',
    'js'                                   : 'JavaScript',
    'typescript'                           : 'TypeScript',
    'ts'                                   : 'TypeScript',
    'python'                               : 'Python',
    'go'                                   : 'Go',
    'golang'                               : 'Go',
    'rust'                                 : 'Rust',
    'kotlin'                               : 'Kotlin',
    'scala'                                : 'Scala',
    'ruby'                                 : 'Ruby',
    'php'                                  : 'PHP',
    'swift'                                : 'Swift',
    'bash'                                 : 'BASH',
    'shell script'                         : 'BASH',
    'shell scripting'                      : 'BASH',
    'unix shell scripting'                 : 'BASH',
    'powershell'                           : 'PowerShell',
    'perl'                                 : 'Perl',
    'r'                                    : 'R',
    'matlab'                               : 'MATLAB',
    'sql'                                  : 'SQL/MySQL',

    # ── Web Frameworks ────────────────────────────────────────────────────────
    'spring'                               : 'Spring / SpringBoot',
    'spring framework'                     : 'Spring / SpringBoot',
    'spring boot'                          : 'Spring / SpringBoot',
    'springboot'                           : 'Spring / SpringBoot',
    'react'                                : 'React',
    'angular'                              : 'Angular',
    'vue'                                  : 'Vue.js',
    'vue.js'                               : 'Vue.js',
    'node'                                 : 'Node.js',
    'node.js'                              : 'Node.js',
    'nodejs'                               : 'Node.js',
    'django'                               : 'Django',
    'flask'                                : 'Flask',
    'asp.net'                              : 'ASP.NET',
    '.net'                                 : 'ASP.NET',
    'dotnet'                               : 'ASP.NET',
    'express'                              : 'Express.js',
    'express.js'                           : 'Express.js',
    'fastapi'                              : 'FastAPI',
    'fastapi'                              : 'FastAPI',
    'jquery'                               : 'jQuery',
    'html5'                                : 'HTML5',
    'html'                                 : 'HTML5',
    'css'                                  : 'CSS/SASS',
    'sass'                                 : 'CSS/SASS',
    'scss'                                 : 'CSS/SASS',
    'tailwind'                             : 'Tailwind',
    'tailwindcss'                          : 'Tailwind',
    'bootstrap'                            : 'Bootstrap',
    'flutter'                              : 'Flutter',

    # ── Backend Tools ─────────────────────────────────────────────────────────
    'composer'                             : 'Composer',
    'npm'                                  : 'NPM',
    'webpack'                              : 'Webpack',
    'maven'                                : 'Maven',
    'gradle'                               : 'Gradle',
    'pip'                                  : 'pip',
    'poetry'                               : 'Poetry',

    # ── DevOps Platforms ──────────────────────────────────────────────────────
    'docker'                               : 'Docker',
    'kubernetes'                           : 'Kubernetes',
    'k8s'                                  : 'Kubernetes',
    'k3s'                                  : 'Kubernetes',
    'aws'                                  : 'AWS',
    'amazon web services'                  : 'AWS',
    'azure'                                : 'Azure',
    'microsoft azure'                      : 'Azure',
    'gcp'                                  : 'Google Cloud Platform',
    'google cloud'                         : 'Google Cloud Platform',
    'google cloud platform'                : 'Google Cloud Platform',
    'cloudflare'                           : 'Cloudflare',
    'vps'                                  : 'VPS Hosting',
    'vps hosting'                          : 'VPS Hosting',
    'heroku'                               : 'Heroku',

    # ── DevOps Tools ──────────────────────────────────────────────────────────
    'git'                                  : 'Git',
    'github'                               : 'Git',
    'gitlab'                               : 'Git',
    'subversion'                           : 'SVN',
    'svn'                                  : 'SVN',
    'jenkins'                              : 'Jenkins',
    'ci/cd'                                : 'CI/CD',
    'cicd'                                 : 'CI/CD',
    'continuous integration'               : 'CI/CD',
    'continuous deployment'                : 'CI/CD',
    'redis'                                : 'Redis',
    'varnish'                              : 'Varnish',
    'memcached'                            : 'Memcached',

    # ── Testing/QA Tools ──────────────────────────────────────────────────────
    'phpunit'                              : 'PHPUnit',
    'unittest'                             : 'unittest',
    'pytest'                               : 'pytest',
    'jest'                                 : 'Jest',
    'cypress'                              : 'Cypress',
    'selenium'                             : 'Selenium',
    'xdebug'                               : 'Xdebug',
    'junit'                                : 'JUnit',
    'testng'                               : 'TestNG',

    # ── Monitoring/Observability ──────────────────────────────────────────────
    'grafana'                              : 'Grafana',
    'prometheus'                           : 'Prometheus',
    'rollbar'                              : 'Rollbar',
    'sentry'                               : 'Sentry',
    'datadog'                              : 'Datadog',
    'new relic'                            : 'New Relic',
    'google analytics'                     : 'Google Analytics',
    'looker'                               : 'Looker',

    # ── CMS/E-Commerce ───────────────────────────────────────────────────────
    'wordpress'                            : 'WordPress',
    'woocommerce'                          : 'WooCommerce',
    'shopify'                              : 'Shopify',
    'magento'                              : 'Magento',
    'pim'                                  : 'PIM & CMS Architecture',
    'plm'                                  : 'PIM & CMS Architecture',
    'content management'                   : 'PIM & CMS Architecture',

    # ── Databases ─────────────────────────────────────────────────────────────
    'mysql'                                : 'MySQL',
    'postgresql'                           : 'PostgreSQL',
    'postgres'                             : 'PostgreSQL',
    'sql server'                           : 'SQL Server',
    'sqlserver'                            : 'SQL Server',
    'mongodb'                              : 'MongoDB',
    'cassandra'                            : 'Cassandra',
    'elasticsearch'                        : 'Elasticsearch',
    'oracle'                               : 'Oracle',
    'oracle database'                      : 'Oracle',
    'mariadb'                              : 'MariaDB',
    'dynamodb'                             : 'DynamoDB',

    # ── Protocols & Formats ───────────────────────────────────────────────────
    'rest'                                 : 'REST API',
    'rest api'                             : 'REST API',
    'restful'                              : 'REST API',
    'api'                                  : 'REST API',
    'soap'                                 : 'SOAP',
    'wsdl'                                 : 'SOAP',
    'graphql'                              : 'GraphQL',
    'grpc'                                 : 'gRPC',
    'xml'                                  : 'XML',
    'json'                                 : 'JSON',
    'javascript object notation'           : 'JSON',
    'yaml'                                 : 'YAML',
    'protobuf'                             : 'Protocol Buffers',
    'avro'                                 : 'Apache Avro',

    # ── Practices & Methodologies ─────────────────────────────────────────────
    'agile'                                : 'Agile',
    'scrum'                                : 'Scrum/Agile',
    'scrum/agile'                          : 'Scrum/Agile',
    'kanban'                               : 'Kanban',
    'devops'                               : 'DevOps',
    'tdd'                                  : 'Test-Driven Development',
    'test-driven development'              : 'Test-Driven Development',
    'bdd'                                  : 'Behavior-Driven Development',
    'oop'                                  : 'Object-Oriented Programming',
    'object-oriented'                      : 'Object-Oriented Programming',
    'functional programming'               : 'Functional Programming',
    'reactive programming'                 : 'Reactive Programming',
    'microservices'                        : 'Microservices',
    'monolith'                             : 'Monolithic Architecture',
    'clean code'                           : 'Clean Code',
    'design patterns'                      : 'Design Patterns',
    'solid principles'                     : 'SOLID Principles',

    # ── Design Tools ──────────────────────────────────────────────────────────
    'figma'                                : 'Figma',
    'adobe creative suite'                 : 'Adobe Creative Suite',
    'photoshop'                            : 'Adobe Creative Suite',
    'illustrator'                          : 'Adobe Creative Suite',
    'xd'                                   : 'Adobe XD',
    'adobe xd'                             : 'Adobe XD',
    'sketch'                               : 'Sketch',
    'invision'                             : 'InVision',

    # ── Project Management Tools ──────────────────────────────────────────────
    'jira'                                 : 'Jira',
    'confluence'                           : 'Confluence',
    'trello'                               : 'Trello',
    'asana'                                : 'Asana',
    'monday'                               : 'Monday.com',
    'monday.com'                           : 'Monday.com',
    'slack'                                : 'Slack',
    'teams'                                : 'Microsoft Teams',
    'microsoft teams'                      : 'Microsoft Teams',
    'discord'                              : 'Discord',
    'zoom'                                 : 'Zoom',
    'google workspace'                     : 'Google Workspace',

    # ── Soft Skills & Domain ──────────────────────────────────────���───────────
    'communication'                        : 'Communication',
    'teamwork'                             : 'Teamwork',
    'project management'                   : 'Project Management',
    'leadership'                           : 'Leadership',
    'mentoring'                            : 'Mentoring',
    'problem solving'                      : 'Problem-Solving',
    'analytical'                           : 'Analytical Thinking',
    'critical thinking'                    : 'Critical Thinking',
    'time management'                      : 'Time Management',
    'attention to detail'                  : 'Attention to Detail',
    'software testing'                     : 'Software Testing & QA',
    'software quality assurance'           : 'Software Testing & QA',
    'qa'                                   : 'Software Testing & QA',
    'usability testing'                    : 'Usability Testing',
    'software design'                      : 'Software Design',
    'network security'                     : 'Network Security',
    'cybersecurity'                        : 'Network Security',
    'security'                             : 'Network Security',
    'embedded systems'                     : 'Embedded Systems',
    'firmware'                             : 'Embedded Systems',
    'device driver'                        : 'Embedded Systems',
    'networking'                           : 'Computer Networking',
    'computer networking'                  : 'Computer Networking',
}


# ════════════════════════════════════════════════════════════════════════════════
# STAGE 1: LOAD & INDEX
# ════════════════════════════════════════════════════════════════════════════════

def load_skills_index(skills_index_path: str = SKILLS_INDEX_PATH) -> Dict:
    """
    Load skills-index.json and build lookup dictionaries.
    
    Returns:
        dict with keys:
          - 'facet_by_name': {normalized_name → facet_entry}
          - 'facet_by_id': {facet_id → facet_entry}
          - 'raw_index': raw skills-index.json data
    """
    with open(skills_index_path, 'r') as f:
        raw_index = json.load(f)

    facet_by_name = {}
    facet_by_id = {}

    for entry in raw_index.get('facet_catalog', []):
        key = entry['facet_name'].lower().strip()
        facet_by_name[key] = entry
        facet_by_id[entry['facet_id']] = entry

    return {
        'facet_by_name': facet_by_name,
        'facet_by_id': facet_by_id,
        'raw_index': raw_index,
    }


# ════════════════════════════════════════════════════════════════════════════════
# STAGE 2: HTML EXTRACTION
# ════════════════════════════════════════════════════════════════════════════════

def extract_skills_from_posting(html_path: str) -> Dict[str, List[str]]:
    """
    Parse Job Bank HTML and extract skills+requirements grouped by section.
    
    Args:
        html_path: Path to HTML file
    
    Returns:
        dict: {section_label → [skill_strings]}
    """
    with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    sections: Dict[str, List[str]] = {}

    def collect_ul(div_id: str, label: str) -> None:
        """Helper: extract all <h4> + <ul> items under a div"""
        div = soup.find('div', id=div_id)
        if not div:
            return
        for h4 in div.find_all('h4'):
            section_label = f"{label} > {h4.get_text(strip=True)}"
            items = []
            ul = h4.find_next_sibling('ul')
            if ul:
                for li in ul.find_all('li'):
                    text_spans = li.find_all('span')
                    text = text_spans[-1].get_text(strip=True) if text_spans else li.get_text(strip=True)
                    if text:
                        items.append(text)
            if items:
                sections[section_label] = items

    # ── Overview section ──────────────────────────────────────────────────────
    chart = soup.find('div', id='comparisonchart')
    if chart:
        # Languages
        lang_h4 = chart.find('h4', string='Languages')
        if lang_h4:
            p = lang_h4.find_next_sibling('p')
            if p:
                sections['Overview > Languages'] = [p.get_text(strip=True)]

        # Education
        edu_h4 = chart.find('h4', string='Education')
        if edu_h4:
            ul = edu_h4.find_next_sibling('ul')
            if ul:
                sections['Overview > Education'] = [
                    li.find_all('span')[-1].get_text(strip=True)
                    if li.find_all('span') else li.get_text(strip=True)
                    for li in ul.find_all('li')
                ]

        # Experience
        exp_h4 = chart.find('h4', string='Experience')
        if exp_h4:
            p = exp_h4.find_next_sibling('p')
            if p:
                spans = p.find_all('span')
                text = next(
                    (s.get_text(strip=True) for s in spans
                     if 'wb-inv' not in (s.get('class') or [])
                     and not any('fa-' in c for c in (s.get('class') or []))),
                    ''
                )
                if text:
                    sections['Overview > Experience'] = [text]

        # Work setting
        ws_div = chart.find('div', id='jobOverview-1')
        if ws_div:
            ul = ws_div.find('ul')
            if ul:
                sections['Overview > Work setting'] = [
                    li.get_text(strip=True) for li in ul.find_all('li')
                ]

    # ── Detailed sections ─────────────────────────────────────────────────────
    collect_ul('jobOverview-2', 'Responsibilities')
    collect_ul('jobOverview-4', 'Experience & Specialization')
    collect_ul('jobOverview-5', 'Additional Information')
    collect_ul('jobOverview-7', 'Benefits')

    return sections


# ════════════════════════════════════════════════════════════════════════════════
# STAGE 3: SKILL RESOLUTION
# ════════════════════════════════════════════════════════════════════════════════

def resolve_facet(raw_skill: str, index: Dict) -> Optional[Dict]:
    """
    Try to map a raw skill string to a facet entry.
    
    Strategy (three-tier resolution):
      1. Exact match on normalized facet_name
      2. Alias table lookup → then exact match
      3. Substring match (conservative: len > 2 to avoid noise)
    
    Args:
        raw_skill: Raw skill string from job posting
        index: Result from load_skills_index()
    
    Returns:
        Facet entry dict, or None if no match found
    """
    facet_by_name = index['facet_by_name']
    normalized = raw_skill.lower().strip()

    # 1. Direct exact match
    if normalized in facet_by_name:
        return facet_by_name[normalized]

    # 2. Alias lookup
    aliased = ALIASES.get(normalized)
    if aliased:
        aliased_normalized = aliased.lower().strip()
        if aliased_normalized in facet_by_name:
            return facet_by_name[aliased_normalized]

    # 3. Substring match (conservative)
    if len(normalized) > 2:
        for fname, entry in facet_by_name.items():
            if normalized in fname or fname in normalized:
                return entry

    return None


# ════════════════════════════════════════════════════════════════════════════════
# STAGE 4: MATCHING REPORT GENERATION
# ════════════════════════════════════════════════════════════════════════════════

def match_posting_to_skills(sections: Dict[str, List[str]], index: Dict) -> Dict:
    """
    For every extracted skill, attempt to resolve against skills index.
    Return structured match report.
    
    Args:
        sections: Result from extract_skills_from_posting()
        index: Result from load_skills_index()
    
    Returns:
        dict with keys:
          - 'summary': stats (total, matched, unmatched, %)
          - 'matched': list of matched skill records
          - 'unmatched': list of unmatched skill records
    """
    matched: List[Dict] = []
    unmatched: List[Dict] = []

    # Flatten extracted skills, tagging each with source section
    skill_rows: List[Tuple[str, str]] = []

    # Sections we want to skill-match (skip education/experience years/benefits)
    skill_sections = {
        'Responsibilities',
        'Experience & Specialization',
        'Additional Information',
        'Overview > Work setting',
    }

    for section_label, items in sections.items():
        is_skill_section = any(s in section_label for s in skill_sections)
        if not is_skill_section:
            continue
        for raw in items:
            skill_rows.append((section_label, raw))

    seen_facet_ids: set = set()

    for section_label, raw_skill in skill_rows:
        entry = resolve_facet(raw_skill, index)
        if entry:
            facet_id = entry['facet_id']
            record = {
                'raw_skill': raw_skill,
                'source_section': section_label,
                'facet_id': facet_id,
                'facet_name': entry['facet_name'],
                'facet_type': entry['facet_type'],
                'skill_group': entry.get('skill_group', 'n/a'),
                'proficiency': entry.get('proficiency', 'n/a'),
                'confidence': entry.get('confidence_level', 'n/a'),
                'years': entry.get('years_of_experience', 'n/a'),
                'last_used': entry.get('last_used', 'n/a'),
                'duplicate': facet_id in seen_facet_ids,
            }
            matched.append(record)
            seen_facet_ids.add(facet_id)
        else:
            unmatched.append({
                'raw_skill': raw_skill,
                'source_section': section_label,
            })

    unique_matched = [r for r in matched if not r['duplicate']]

    return {
        'summary': {
            'total_skills_extracted': len(skill_rows),
            'matched_to_facets': len(unique_matched),
            'unmatched': len(unmatched),
            'match_rate_pct': round(len(unique_matched) / max(len(skill_rows), 1) * 100, 1),
        },
        'matched': matched,
        'unmatched': unmatched,
    }


# ════════════════════════════════════════════════════════════════════════════════
# STAGE 5: REPORTING
# ════════════════════════════════════════════════════════════════════════════════

def print_report(report: Dict, sections: Dict) -> None:
    """Pretty-print match report to console."""
    s = report['summary']
    print("\n" + "═" * 80)
    print("  JOB POSTING ↔ SKILLS INDEX MATCH REPORT")
    print("═" * 80)
    print(f"  Skills extracted : {s['total_skills_extracted']}")
    print(f"  Matched          : {s['matched_to_facets']}")
    print(f"  Unmatched        : {s['unmatched']}")
    print(f"  Match rate       : {s['match_rate_pct']}%")
    print("═" * 80)

    print("\n── MATCHED SKILLS ──────────────────────────────────────────────────────────")
    for r in report['matched']:
        dup_tag = " [duplicate]" if r['duplicate'] else ""
        print(
            f"  ✓ {r['raw_skill']:<40} "
            f"→ {r['facet_name']:<30} "
            f"[{r['facet_type']}] "
            f"yrs={r['years']} conf={r['confidence']}"
            f"{dup_tag}"
        )

    if report['unmatched']:
        print("\n── UNMATCHED SKILLS (gaps / new aliases needed) ──────────────────────────")
        for r in report['unmatched']:
            print(f"  ✗ {r['raw_skill']:<40}  ({r['source_section']})")

    print("\n── EXTRACTED SECTIONS (raw) ────────────────────────────────────────────────")
    for section, items in sections.items():
        print(f"\n  [{section}]")
        for item in items[:5]:  # Show first 5 items per section
            print(f"    • {item}")
        if len(items) > 5:
            print(f"    ... and {len(items) - 5} more")


def save_match_report(
    html_path: str,
    sections: Dict[str, List[str]],
    report: Dict,
    output_path: Optional[str] = None
) -> str:
    """
    Save full match report to JSON file.
    
    Args:
        html_path: Source HTML file
        sections: Extracted sections
        report: Match report
        output_path: Output file path (default: html_path with .json extension)
    
    Returns:
        Path to created JSON file
    """
    if output_path is None:
        output_path = Path(html_path).stem + '.json'

    output = {
        'metadata': {
            'source': 'Job Bank Canada',
            'extracted_date': datetime.now().isoformat() + 'Z',
            'source_html': html_path,
        },
        'extracted_sections': sections,
        'match_report': report,
    }

    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    return output_path


# ════════════════════════════════════════════════════════════════════════════════
# ORCHESTRATION
# ════════════════════════════════════════════════════════════════════════════════

def analyze_job_posting(html_path: str, verbose: bool = True) -> Dict:
    """
    End-to-end pipeline: extract + match + report.
    
    Args:
        html_path: Path to job posting HTML
        verbose: Print report to console
    
    Returns:
        dict: {sections, report, output_file}
    """
    index = load_skills_index()
    sections = extract_skills_from_posting(html_path)
    report = match_posting_to_skills(sections, index)

    if verbose:
        print_report(report, sections)

    output_file = save_match_report(html_path, sections, report)

    return {
        'sections': sections,
        'report': report,
        'output_file': output_file,
    }


def batch_analyze_job_postings(job_dir: str = JOB_HTML_DIR, verbose: bool = True) -> List[Dict]:
    """
    Analyze all HTML files in a directory.
    
    Args:
        job_dir: Directory containing HTML files
        verbose: Print reports to console
    
    Returns:
        list of analysis results (one per HTML file)
    """
    job_path = Path(job_dir)
    html_files = sorted(job_path.glob('*.html'))

    print(f"\n{'='*80}")
    print(f"  BATCH ANALYSIS: {len(html_files)} job postings")
    print(f"{'='*80}\n")

    results = []
    for html_file in html_files:
        print(f"Analyzing: {html_file.name}")
        try:
            result = analyze_job_posting(str(html_file), verbose=verbose)
            results.append({
                'file': html_file.name,
                'success': True,
                'result': result,
            })
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                'file': html_file.name,
                'success': False,
                'error': str(e),
            })

    # Summary
    successful = sum(1 for r in results if r['success'])
    print(f"\n{'='*80}")
    print(f"  Completed: {successful}/{len(html_files)} successful")
    print(f"{'='*80}\n")

    return results


# ════════════════════════════════════════════════════════════════════════════════
# CLI USAGE
# ════════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        # Single file mode
        html_file = sys.argv[1]
        print(f"\nAnalyzing: {html_file}\n")
        analyze_job_posting(html_file, verbose=True)
    else:
        # Batch mode
        batch_analyze_job_postings(verbose=False)

        # Print summary
        print("\nGenerating unified summary...")
        job_path = Path(JOB_HTML_DIR)
        json_files = list(job_path.glob('*.json'))

        print(f"\nCreated {len(json_files)} match reports:")
        for jf in sorted(json_files):
            print(f"  • {jf.name}")
