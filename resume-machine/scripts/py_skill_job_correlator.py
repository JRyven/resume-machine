import json
import re
from pathlib import Path
from datetime import datetime

# ── Config ─────────────────────────────────────────────────────────────────────
import sys

# Defaults (can be overridden by CLI args)
SKILLS_INDEX_PATH = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/resume-machine/skills-index.json'
JOB_JSON_PATH     = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/04/05/software developer - Kanata, ON - Job posting - Job Bank.json'
OUTPUT_PATH       = '/Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/jobbankjobs/2026/04/05/correlation_software_developer_kanata.json'

# ── Thresholds ─────────────────────────────────────────────────────────────────
STALE_YEAR_THRESHOLD  = 2      # last_used older than N years ago = UNTESTED_CLAIM
LEAD_CONFIDENCE_MIN   = 8      # confidence >= this = LEAD_STRENGTH candidate
LEAD_YEARS_MULTIPLIER = 1.5    # your years >= job_required_years * this = LEAD_STRENGTH
PARTIAL_CONFIDENCE_MAX = 6     # confidence <= this = PARTIAL_MATCH ceiling

CURRENT_YEAR = datetime.now().year
CURRENT_QUARTER = f"{CURRENT_YEAR}-Q{((datetime.now().month - 1) // 3) + 1}"

# ── Facet type weights (higher = more important signal for this role type) ─────
FACET_TYPE_WEIGHTS = {
    'hands_on_language'    : 1.0,
    'hands_on_framework'   : 0.9,
    'hands_on_tool'        : 0.8,
    'hands_on_platform'    : 0.8,
    'hands_on_skill'       : 0.7,
    'strategic_domain'     : 0.9,
    'leadership_soft_skill': 0.6,
}

# ── Alias table: job posting term → canonical facet_name (lowercase) ───────────
ALIASES: dict[str, str] = {
    # Languages
    'c'                                        : 'php',          # no C facet; nearest compiled-lang
    'c++'                                      : 'php',
    'c#'                                       : 'php',
    'java'                                     : 'javascript',   # adjacency — JVM vs JS ecosystem
    'javascript'                               : 'javascript',
    'typescript'                               : 'javascript',
    'python'                                   : 'python',
    'go'                                       : 'php',
    'golang'                                   : 'php',
    'rust'                                     : 'php',
    'kotlin'                                   : 'javascript',
    'scala'                                    : 'javascript',
    'ruby'                                     : 'php',
    'php'                                      : 'php',
    'swift'                                    : 'javascript',
    'bash'                                     : 'bash',
    'shell script'                             : 'bash',
    'unix shell scripting'                     : 'bash',
    'powershell'                               : 'bash',

    # Frameworks
    'spring'                                   : 'node.js',      # server-side framework adjacency
    'spring framework'                         : 'node.js',
    'spring boot'                              : 'node.js',
    'react'                                    : 'react',
    'angular'                                  : 'react',
    'vue'                                      : 'react',
    'node'                                     : 'node.js',
    'node.js'                                  : 'node.js',
    'django'                                   : 'node.js',
    'flask'                                    : 'node.js',
    'asp.net'                                  : 'node.js',
    '.net'                                     : 'node.js',
    'express'                                  : 'node.js',
    'fastapi'                                  : 'node.js',
    'jsp'                                      : 'node.js',
    'servlet'                                  : 'node.js',
    'junit'                                    : 'phpunit',      # test framework adjacency
    'testng'                                   : 'phpunit',
    'jest'                                     : 'jest',
    'cypress'                                  : 'cypress',

    # Tools
    'git'                                      : 'git',
    'subversion'                               : 'svn',
    'subversion (svn)'                         : 'svn',
    'svn'                                      : 'svn',
    'jenkins'                                  : 'ci/cd',        # CI tool → CI/CD facet
    'jira'                                     : 'jira',
    'confluence'                               : 'confluence',
    'docker'                                   : 'docker',
    'kubernetes'                               : 'kubernetes',
    'k8s'                                      : 'kubernetes',
    'terraform'                                : 'docker',       # IaC adjacency
    'ansible'                                  : 'docker',
    'sonarqube'                                : 'phpunit',      # QA tooling adjacency
    'maven'                                    : 'npm',
    'gradle'                                   : 'npm',
    'npm'                                      : 'npm',
    'webpack'                                  : 'webpack',
    'postman'                                  : 'xdebug',       # API debugging adjacency
    'redis'                                    : 'redis',
    'varnish'                                  : 'varnish',
    'composer'                                 : 'composer',
    'figma'                                    : 'figma',
    'sketch'                                   : 'sketch',

    # Platforms / cloud
    'aws'                                      : 'aws',
    'azure'                                    : 'aws',          # cloud platform adjacency
    'microsoft azure'                          : 'aws',
    'gcp'                                      : 'aws',
    'google cloud'                             : 'aws',
    'linux'                                    : 'vps hosting',
    'ubuntu'                                   : 'vps hosting',
    'unix'                                     : 'vps hosting',
    'windows'                                  : 'vps hosting',
    'ms windows'                               : 'vps hosting',
    'cloud'                                    : 'aws',
    'cloudflare'                               : 'cloudflare',

    # Databases
    'sql'                                      : 'sql/mysql',
    'mysql'                                    : 'sql/mysql',
    'sql/mysql'                                : 'sql/mysql',
    'postgresql'                               : 'sql/mysql',
    'sql server'                               : 'sql/mysql',
    'mongodb'                                  : 'sql/mysql',
    'redis'                                    : 'redis',
    'elasticsearch'                            : 'sql/mysql',
    'cassandra'                                : 'sql/mysql',
    'oracle'                                   : 'sql/mysql',

    # Protocols / formats
    'rest'                                     : 'node.js',
    'rest api'                                 : 'node.js',
    'soap'                                     : 'node.js',
    'graphql'                                  : 'node.js',
    'grpc'                                     : 'node.js',
    'xml'                                      : 'javascript',
    'json'                                     : 'javascript',
    'javascript object notation (json)'        : 'javascript',
    'xml technology (xsl,xsd,dtd)'             : 'javascript',
    'tcp/ip'                                   : 'vps hosting',
    'api'                                      : 'node.js',

    # Practices
    'agile'                                    : 'scrum/agile',
    'scrum'                                    : 'scrum/agile',
    'scrum/agile'                              : 'scrum/agile',
    'devops'                                   : 'ci/cd',
    'ci/cd'                                    : 'ci/cd',
    'tdd'                                      : 'phpunit',
    'test-driven development'                  : 'phpunit',
    'object-oriented'                          : 'javascript',
    'object-oriented programming languages'    : 'javascript',
    'microservices'                            : 'docker',
    'software development'                     : 'ci/cd',
    'software quality assurance'               : 'phpunit',
    'usability testing'                        : 'figma',
    'information technology infrastructure library (itil)': 'company policy & governance',

    # Domain / soft
    'project management'                       : 'jira',
    'project implementation'                   : 'jira',
    'communication'                            : 'presentations',
    'teamwork'                                 : 'meeting facilitation',
    'problem solving'                          : 'consensus building',
    'design'                                   : 'pim & cms architecture',
    'user experience design'                   : 'figma',
    'development of computer applications'     : 'php',
    'testing'                                  : 'phpunit',
    'quality assurance or control'             : 'phpunit',
    'embedded systems'                         : 'vps hosting',
    'firmware development'                     : 'vps hosting',
    'networking'                               : 'vps hosting',
    'networking software'                      : 'vps hosting',
    'networking hardware'                      : 'vps hosting',
    'networking security'                      : 'vps hosting',
    'device drivers'                           : 'vps hosting',
    'ms office'                                : 'google workspace',
    'ms excel'                                 : 'google workspace',
    'spreadsheet'                              : 'google workspace',
    'airline company'                          : 'company policy & governance',

    # Tasks → skill adjacencies
    'collect and document user\'s requirements'                             : 'confluence',
    'coordinate the development, installation, integration and operation of computer-based systems': 'ci/cd',
    'define system functionality'                                           : 'pim & cms architecture',
    'develop flowcharts, layouts and documentation to identify solutions'   : 'figma',
    'develop process and network models to optimize architecture'           : 'pim & cms architecture',
    'evaluate the performance and reliability of system designs'            : 'grafana',
    'evaluate user feedback'                                                : 'google analytics',
    'execute full lifecycle software development'                           : 'ci/cd',
    'plan every step of the integration of a computer-based system'        : 'jira',
    'prepare plan to maintain software'                                     : 'confluence',
    'research technical information to design, develop and test computer-based systems': 'pim & cms architecture',
    'synthesize technical information for every phase of the cycle of a computer-based system': 'pim & cms architecture',
    'upgrade and maintain software'                                         : 'ci/cd',
    'lead and co-ordinate teams of information systems professionals in the development of software and integrated information systems, process control software and other embedded software control systems': 'mentoring',
    'usability testing'                                                     : 'figma',
    'operate automatic or other testing equipment to ensure product quality': 'phpunit',
    'consult with clients after sale to provide ongoing support'            : 'sales meetings',
    'conduct tests and perform security and quality controls'               : 'phpunit',
    'execute and document results of software application tests and information and telecommunication systems tests': 'phpunit',
}

# ── Explicit adjacency map: facet_name (lower) → list of adjacent facet_names ──
# Used when a job needs X and you have Y (related but not identical)
# All keys should be lowercase for consistent lookup
ADJACENCY_MAP: dict[str, list[str]] = {
    'java'           : ['javascript', 'php', 'node.js'],
    'spring framework': ['node.js', 'php'],
    'junit'          : ['phpunit', 'jest', 'cypress'],
    'testng'         : ['phpunit', 'jest'],
    'jenkins'        : ['ci/cd', 'git'],
    'terraform'      : ['docker', 'kubernetes', 'aws'],
    'ansible'        : ['docker', 'aws'],
    'sonarqube'      : ['phpunit', 'xdebug'],
    'maven'          : ['npm', 'composer'],
    'gradle'         : ['npm', 'composer'],
    'angular'        : ['react', 'javascript'],
    'vue'            : ['react', 'javascript'],
    'typescript'     : ['javascript'],
    'kotlin'         : ['javascript', 'php'],
    'scala'          : ['javascript'],
    'graphql'        : ['node.js'],
    'grpc'           : ['node.js'],
    'elasticsearch'  : ['sql/mysql', 'redis'],
    'postgresql'     : ['sql/mysql'],
    'mongodb'        : ['sql/mysql', 'redis'],
    'azure'          : ['aws', 'cloudflare'],
    'gcp'            : ['aws'],
    'itil'           : ['company policy & governance', 'jira'],
    'information technology infrastructure library (itil)': ['company policy & governance'],
    'user experience design': ['figma', 'sketch'],
    'usability testing': ['figma', 'cypress', 'phpunit'],
    'jsp'            : ['node.js', 'php'],
    'servlet'        : ['node.js', 'php'],
    'shell script'   : ['bash'],
    'subversion (svn)': ['svn', 'git'],
}

# ── Extract job required years from overview.experience ───────────────────────
def parse_required_years(exp_str: str) -> int:
    """Parse '5 years or more' → 5"""
    match = re.search(r'(\d+)', exp_str or '')
    return int(match.group(1)) if match else 0

# ── Pull all skill terms from the job JSON ─────────────────────────────────────
def extract_job_terms(job_data: dict) -> list[tuple[str, str, int]]:
    """
    Returns list of (term, source_section, section_weight).
    section_weight reflects how strongly that section signals a core requirement.
    """
    terms: list[tuple[str, str, int]] = []

    # Section weight map: higher = more important for job fit
    SECTION_WEIGHTS = {
        'required_skills'    : 3,
        'additional_skills'  : 2,
        'specialization'     : 3,
        'responsibilities'   : 2,
        'overview'           : 1,
        'benefits'           : 0,  # Skip benefits section
    }

    # Extract from job_posting sections
    job_posting = job_data.get('job_posting', {}) or {}

    for section, items_or_dict in job_posting.items():
        weight = SECTION_WEIGHTS.get(section, 1)

        if weight == 0:  # Skip benefits, etc.
            continue

        if isinstance(items_or_dict, dict):
            # Nested dict: specialization > Computer and technology knowledge
            for subsection, items in items_or_dict.items():
                if isinstance(items, list):
                    for item in items:
                        if item and isinstance(item, str):
                            terms.append((item.lower().strip(), f'{section}.{subsection}', weight))
        elif isinstance(items_or_dict, list):
            # Flat list
            for item in items_or_dict:
                if item and isinstance(item, str):
                    terms.append((item.lower().strip(), section, weight))

    # Extract from required_skills (matched skills dict)
    for facet_id, skill_data in job_data.get('required_skills', {}).items():
        if isinstance(skill_data, dict):
            facet_name = skill_data.get('facet_name', '')
            if facet_name:
                terms.append((facet_name.lower().strip(), 'required_skills', 3))

    # Extract from additional_skills (unmatched skills dict)
    for facet_id, skill_data in job_data.get('additional_skills', {}).items():
        if isinstance(skill_data, dict):
            facet_name = skill_data.get('facet_name', '')
            if facet_name:
                terms.append((facet_name.lower().strip(), 'additional_skills', 2))

    return terms

# ── Resolve a job term to a facet entry ───────────────────────────────────────
def resolve_to_facet(term: str, facet_lookup: dict):
    """
    Returns (facet_entry, has_adjacent_alternative).

    facet_entry: Direct match found (direct or via alias)
    has_adjacent_alternative: No direct match, but adjacency map suggests related skill

    Note: Never returns a facet for an adjacency match. Adjacency is signaled via
    the boolean flag so it can be tagged GAP_ADJACENCY in scoring.
    """
    term_lower = term.lower().strip()

    # 1. Direct facet name match
    if term_lower in facet_lookup:
        return facet_lookup[term_lower], False

    # 2. Alias → facet name
    aliased = ALIASES.get(term_lower, '').lower()
    if aliased and aliased in facet_lookup:
        return facet_lookup[aliased], False

    # 3. Substring fallback (conservative)
    if len(term_lower) > 4:
        for fname, entry in facet_lookup.items():
            if term_lower in fname or fname in term_lower:
                return entry, False

    # 4. Check adjacency map (but don't return the adjacent facet as a match)
    # Instead, signal that an adjacent skill exists
    adj_candidates = ADJACENCY_MAP.get(term_lower, [])
    if adj_candidates:
        # Check if we own any of the adjacent skills
        for adj_name in adj_candidates:
            if adj_name in facet_lookup and facet_lookup[adj_name].get('proficiency'):
                # We have an adjacent skill, but signal this via return (None, True)
                return None, True

    # No match found
    return None, False

# ── Compute content tag ────────────────────────────────────────────────────────
def compute_content_tag(
    facet: dict,
    is_adjacent: bool,
    section_weight: int,
    job_required_years: int,
    mention_count: int,
) -> tuple[str, float]:
    """
    Returns (content_tag, score).
    Score is used to rank correlations within the same tag tier.
    """
    if facet is None:
        return 'HARD_GAP', 0.0

    confidence    = facet.get('confidence_level') or 0
    years         = facet.get('years_of_experience') or 0
    proficiency   = facet.get('proficiency') or 'novice'
    last_used_str = facet.get('last_used') or ''
    facet_type    = facet.get('facet_type') or 'hands_on_skill'
    type_weight   = FACET_TYPE_WEIGHTS.get(facet_type, 0.7)

    # Staleness check
    stale = False
    if last_used_str:
        try:
            last_year = int(last_used_str.split('-')[0])
            stale = (CURRENT_YEAR - last_year) >= STALE_YEAR_THRESHOLD
        except ValueError:
            pass

    prof_rank = {'novice': 1, 'beginner': 2, 'intermediate': 3,
                 'advanced': 4, 'expert': 5}.get(proficiency, 1)

    # Base score
    score = (
        (confidence / 10.0) * 0.35 +
        (prof_rank  / 5.0)  * 0.30 +
        (min(years, 15) / 15.0) * 0.20 +
        (mention_count / 5.0)   * 0.10 +
        (section_weight / 3.0)  * 0.05
    ) * type_weight

    # Adjacency penalty
    if is_adjacent:
        score *= 0.65

    # Assign tag
    if is_adjacent:
        tag = 'GAP_ADJACENCY'
    elif stale:
        tag = 'UNTESTED_CLAIM'
    elif (confidence >= LEAD_CONFIDENCE_MIN and
          prof_rank >= 4 and
          years >= job_required_years * LEAD_YEARS_MULTIPLIER):
        tag = 'LEAD_STRENGTH'
    elif confidence >= 7 and prof_rank >= 3:
        tag = 'SOLID_MATCH'
    elif confidence <= PARTIAL_CONFIDENCE_MAX or prof_rank <= 2:
        tag = 'PARTIAL_MATCH'
    else:
        tag = 'SOLID_MATCH'

    return tag, round(score, 4)

# ── Main correlation procedure ─────────────────────────────────────────────────
def build_correlation_report(job_data: dict, skills_index: dict, facet_lookup: dict) -> dict:

    job_posting = job_data.get('job_posting', job_data)
    job_required_years = parse_required_years(
        job_posting.get('overview', {}).get('experience', '0')
    )

    terms = extract_job_terms(job_data)

    # Track facets by enriched metadata
    facet_mention_counts: dict[str, int] = {}
    facet_section_weights: dict[str, int] = {}
    facet_adjacency_available: dict[str, bool] = {}
    facet_sources: dict[str, list[str]] = {}
    facet_by_term: dict[str, dict] = {}  # term → resolved facet entry

    # First pass: resolve and aggregate mentions
    for term, section, weight in terms:
        entry, has_adjacent = resolve_to_facet(term, facet_lookup)

        if entry is not None:
            # Direct match found
            fname = entry['facet_name'].lower()
            facet_mention_counts[fname] = facet_mention_counts.get(fname, 0) + 1
            facet_section_weights[fname] = max(facet_section_weights.get(fname, 0), weight)
            if fname not in facet_adjacency_available:
                facet_adjacency_available[fname] = False
            facet_sources.setdefault(fname, [])
            if section not in facet_sources[fname]:
                facet_sources[fname].append(section)
            facet_by_term[fname] = entry
        elif has_adjacent:
            # Adjacency alternative exists (but no direct match)
            # Mark this gap as having adjacency available
            facet_mention_counts[term] = facet_mention_counts.get(term, 0) + 1
            facet_section_weights[term] = max(facet_section_weights.get(term, 0), weight)
            facet_adjacency_available[term] = True
            facet_sources.setdefault(term, [])
            if section not in facet_sources[term]:
                facet_sources[term].append(section)

    # Find unresolved terms (HARD_GAP candidates)
    hard_gaps: list[dict] = []
    seen_resolved: set[str] = set(facet_mention_counts.keys())

    for term, section, weight in terms:
        if term not in seen_resolved:
            entry, has_adj = resolve_to_facet(term, facet_lookup)

    # Build correlation records
    correlations: list[dict] = []

    for fname_or_term, mention_count in facet_mention_counts.items():
        facet = facet_by_term.get(fname_or_term)
        is_adj = facet_adjacency_available.get(fname_or_term, False)
        sec_weight = facet_section_weights.get(fname_or_term, 1)
        sources = facet_sources.get(fname_or_term, [])

        tag, score = compute_content_tag(
            facet, is_adj, sec_weight, job_required_years, mention_count
        )

        correlations.append({
            'facet_id'           : facet.get('facet_id') if facet else None,
            'facet_name'         : facet.get('facet_name') if facet else fname_or_term,
            'facet_type'         : facet.get('facet_type') if facet else None,
            'skill_group'        : facet.get('skill_group') if facet else None,
            'content_tag'        : tag,
            'score'              : score,
            'mention_count'      : mention_count,
            'source_sections'    : sources,
            'is_adjacent_match'  : is_adj,
            'your_proficiency'   : facet.get('proficiency') if facet else None,
            'your_confidence'    : facet.get('confidence_level') if facet else None,
            'your_years'         : facet.get('years_of_experience') if facet else None,
            'your_last_used'     : facet.get('last_used') if facet else None,
            'job_required_years' : job_required_years,
        })

    # Sort: by tag tier then score descending
    TAG_ORDER = {
        'LEAD_STRENGTH' : 0,
        'SOLID_MATCH'   : 1,
        'PARTIAL_MATCH' : 2,
        'UNTESTED_CLAIM': 3,
        'GAP_ADJACENCY' : 4,
        'HARD_GAP'      : 5,
    }
    correlations.sort(key=lambda r: (TAG_ORDER.get(r['content_tag'], 9), -r['score']))

    # Tag frequency summary
    tag_counts: dict[str, int] = {}
    for r in correlations:
        tag_counts[r['content_tag']] = tag_counts.get(r['content_tag'], 0) + 1

    # Deduplicated hard gaps (unique by term)
    seen_gaps: set[str] = set()
    unique_gaps = []
    for g in hard_gaps:
        if g['term'] not in seen_gaps:
            seen_gaps.add(g['term'])
            unique_gaps.append(g)

    return {
        '$schema'        : '../../../resume-machine/skills-schema.json',
        'metadata'       : {
            'generated_at'      : datetime.utcnow().isoformat() + 'Z',
            'job_json'          : JOB_JSON_PATH,
            'skills_index'      : SKILLS_INDEX_PATH,
            'job_title'         : job_posting.get('job_title', ''),
            'employer'          : job_posting.get('employer', ''),
            'job_required_years': job_required_years,
        },
        'summary'        : {
            'total_correlations' : len(correlations),
            'hard_gaps_count'    : len(unique_gaps),
            'tag_distribution'   : tag_counts,
        },
        'correlations'   : correlations,
        'hard_gaps'      : unique_gaps,
    }

# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    try:
        # Allow override of job JSON and output path via CLI args
        # Usage: python py_skill_job_correlator.py [JOB_JSON_PATH] [OUTPUT_PATH]
        job_json_path = JOB_JSON_PATH
        output_path = OUTPUT_PATH
        if len(sys.argv) > 1:
            job_json_path = sys.argv[1]
        if len(sys.argv) > 2:
            output_path = sys.argv[2]

        if not Path(SKILLS_INDEX_PATH).exists():
            print(f"ERROR: Skills index not found at {SKILLS_INDEX_PATH}")
            exit(1)

        if not Path(job_json_path).exists():
            print(f"ERROR: Job JSON not found at {job_json_path}")
            exit(1)

        with open(SKILLS_INDEX_PATH, 'r') as f:
            skills_index = json.load(f)

        with open(job_json_path, 'r') as f:
            job_data = json.load(f)

        # Build facet lookups from skills-index
        facet_lookup = {}
        for entry in skills_index.get('facet_catalog', []):
            key = entry['facet_name'].lower().strip()
            facet_lookup[key] = {**entry, 'proficiency': None, 'confidence_level': None,
                                 'years_of_experience': None, 'last_used': None,
                                 'experience_level': None}
        for skill_group_key, skill_group_list in skills_index.get('skills', {}).items():
            for skill_group in skill_group_list:
                for facet_key, facet_data in skill_group.get('facets', {}).items():
                    fname = facet_data['facet_name'].lower().strip()
                    if fname in facet_lookup:
                        facet_lookup[fname].update({
                            'proficiency'       : facet_data.get('proficiency'),
                            'confidence_level'  : facet_data.get('confidence_level'),
                            'years_of_experience': facet_data.get('years_of_experience'),
                            'last_used'         : facet_data.get('last_used'),
                            'experience_level'  : facet_data.get('experience_level'),
                            'skill_group'       : skill_group_key,
                        })

        print(f"Loaded {len(facet_lookup)} enriched facets from skills index")

        # Build and run the report
        report = build_correlation_report(job_data, skills_index, facet_lookup)

        # Save report
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        # Print summary
        print(f"\n{'═' * 60}")
        print(f"  CORRELATION REPORT")
        print(f"{'═' * 60}")
        print(f"  Job    : {report['metadata']['job_title']}")
        print(f"  Employer: {report['metadata']['employer']}")
        print(f"  Required experience: {report['metadata']['job_required_years']} yrs")
        print(f"{'═' * 60}")

        for tag in ['LEAD_STRENGTH','SOLID_MATCH','PARTIAL_MATCH','UNTESTED_CLAIM','GAP_ADJACENCY']:
            items = [r for r in report['correlations'] if r['content_tag'] == tag]
            if not items:
                continue
            print(f"\n── {tag} ({'─' * (50 - len(tag))})")
            for r in items[:10]:  # Show top 10 per tag
                adj = " [adjacent]" if r['is_adjacent_match'] else ""
                print(
                    f"  {r['facet_name']:<30} "
                    f"prof={str(r['your_proficiency']):<12} "
                    f"conf={str(r['your_confidence']):<4} "
                    f"yrs={str(r['your_years']):<4} "
                    f"score={r['score']:.3f}"
                    f"{adj}"
                )
            if len(items) > 10:
                print(f"  ... and {len(items) - 10} more")

        if report['hard_gaps']:
            print(f"\n── HARD_GAP (terms in job with no facet match) ──────────")
            for g in report['hard_gaps'][:15]:
                print(f"  ✗ {g['term'][:60]:<62} ({g['source_section']})")
            if len(report['hard_gaps']) > 15:
                print(f"  ... and {len(report['hard_gaps']) - 15} more")

        print(f"\n✓ Saved to: {output_path}\n")

    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in input file: {e}")
        exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
