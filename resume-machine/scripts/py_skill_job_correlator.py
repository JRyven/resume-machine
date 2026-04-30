#!/usr/bin/env python3
"""Compatibility shim — forwards to data_processing/py_skill_job_correlator.py"""

import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
NEW = os.path.join(HERE, 'data_processing', 'py_skill_job_correlator.py')
if not os.path.exists(NEW):
        print(f"Error: relocated correlator not found at {NEW}")
        sys.exit(1)

os.execv(sys.executable, [sys.executable, NEW] + sys.argv[1:])

# ── Thresholds ─────────────────────────────────────────────────────────────────
STALE_YEAR_THRESHOLD   = 2      # last_used older than N years → UNTESTED_CLAIM
LEAD_CONFIDENCE_MIN    = 8      # confidence ≥ this → LEAD_STRENGTH candidate
LEAD_YEARS_MULTIPLIER  = 1.5   # your_years ≥ job_years × this → LEAD_STRENGTH
PARTIAL_CONFIDENCE_MAX = 6     # confidence ≤ this → PARTIAL_MATCH ceiling

CURRENT_YEAR    = datetime.now(timezone.utc).year
CURRENT_QUARTER = f"{CURRENT_YEAR}-Q{((datetime.now(timezone.utc).month - 1) // 3) + 1}"

# ── Facet type weights ─────────────────────────────────────────────────────────
FACET_TYPE_WEIGHTS: dict[str, float] = {
    'hands_on_language'     : 1.0,
    'hands_on_framework'    : 0.9,
    'hands_on_tool'         : 0.8,
    'hands_on_platform'     : 0.8,
    'hands_on_skill'        : 0.7,
    'strategic_domain'      : 0.9,
    'leadership_soft_skill' : 0.6,
}

# ── Tag sort order ─────────────────────────────────────────────────────────────
TAG_ORDER: dict[str, int] = {
    'LEAD_STRENGTH'  : 0,
    'SOLID_MATCH'    : 1,
    'PARTIAL_MATCH'  : 2,
    'UNTESTED_CLAIM' : 3,
    'GAP_ADJACENCY'  : 4,
    'HARD_GAP'       : 5,
}

# ── Section weights ────────────────────────────────────────────────────────────
SECTION_WEIGHTS: dict[str, int] = {
    'required_skills'   : 3,
    'additional_skills' : 2,
    'specialization'    : 3,
    'responsibilities'  : 2,
    'overview'          : 1,
    'benefits'          : 0,  # skipped
}

# ── Alias table: job term (lowercase) → canonical facet_name (lowercase) ───────
# These are "nearest facet you actually own" mappings — intentionally lossy for
# adjacency scoring. Prefer ADJACENCY_MAP for skills you hold but don't own exactly.
ALIASES: dict[str, str] = {
    # Languages
    'c'                                        : 'php',
    'c++'                                      : 'php',
    'c#'                                       : 'php',
    'java'                                     : 'javascript',
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
    'spring'                                   : 'node.js',
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
    'junit'                                    : 'phpunit',
    'testng'                                   : 'phpunit',
    'jest'                                     : 'jest',
    'cypress'                                  : 'cypress',

    # Tools
    'git'                                      : 'git',
    'subversion'                               : 'svn',
    'subversion (svn)'                         : 'svn',
    'svn'                                      : 'svn',
    'jenkins'                                  : 'ci/cd',
    'jira'                                     : 'jira',
    'confluence'                               : 'confluence',
    'docker'                                   : 'docker',
    'kubernetes'                               : 'kubernetes',
    'k8s'                                      : 'kubernetes',
    'terraform'                                : 'docker',
    'ansible'                                  : 'docker',
    'sonarqube'                                : 'phpunit',
    'maven'                                    : 'npm',
    'gradle'                                   : 'npm',
    'npm'                                      : 'npm',
    'webpack'                                  : 'webpack',
    'postman'                                  : 'xdebug',
    'redis'                                    : 'redis',
    'varnish'                                  : 'varnish',
    'composer'                                 : 'composer',
    'figma'                                    : 'figma',
    'sketch'                                   : 'sketch',

    # Platforms / cloud
    'aws'                                      : 'aws',
    'azure'                                    : 'aws',
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

    # Long-form task phrases → skill adjacencies
    "collect and document user's requirements"                                                  : 'confluence',
    'coordinate the development, installation, integration and operation of computer-based systems': 'ci/cd',
    'define system functionality'                                                               : 'pim & cms architecture',
    'develop flowcharts, layouts and documentation to identify solutions'                       : 'figma',
    'develop process and network models to optimize architecture'                               : 'pim & cms architecture',
    'evaluate the performance and reliability of system designs'                                : 'grafana',
    'evaluate user feedback'                                                                    : 'google analytics',
    'execute full lifecycle software development'                                               : 'ci/cd',
    'plan every step of the integration of a computer-based system'                            : 'jira',
    'prepare plan to maintain software'                                                         : 'confluence',
    'research technical information to design, develop and test computer-based systems'         : 'pim & cms architecture',
    'synthesize technical information for every phase of the cycle of a computer-based system' : 'pim & cms architecture',
    'upgrade and maintain software'                                                             : 'ci/cd',
    'lead and co-ordinate teams of information systems professionals in the development of software and integrated information systems, process control software and other embedded software control systems': 'mentoring',
    'operate automatic or other testing equipment to ensure product quality'                    : 'phpunit',
    'consult with clients after sale to provide ongoing support'                               : 'sales meetings',
    'conduct tests and perform security and quality controls'                                   : 'phpunit',
    'execute and document results of software application tests and information and telecommunication systems tests': 'phpunit',
}

# ── Adjacency map: job term (lower) → list of facet_names you own as alternatives ─
ADJACENCY_MAP: dict[str, list[str]] = {
    'java'            : ['javascript', 'php', 'node.js'],
    'spring framework': ['node.js', 'php'],
    'junit'           : ['phpunit', 'jest', 'cypress'],
    'testng'          : ['phpunit', 'jest'],
    'jenkins'         : ['ci/cd', 'git'],
    'terraform'       : ['docker', 'kubernetes', 'aws'],
    'ansible'         : ['docker', 'aws'],
    'sonarqube'       : ['phpunit', 'xdebug'],
    'maven'           : ['npm', 'composer'],
    'gradle'          : ['npm', 'composer'],
    'angular'         : ['react', 'javascript'],
    'vue'             : ['react', 'javascript'],
    'typescript'      : ['javascript'],
    'kotlin'          : ['javascript', 'php'],
    'scala'           : ['javascript'],
    'graphql'         : ['node.js'],
    'grpc'            : ['node.js'],
    'elasticsearch'   : ['sql/mysql', 'redis'],
    'postgresql'      : ['sql/mysql'],
    'mongodb'         : ['sql/mysql', 'redis'],
    'azure'           : ['aws', 'cloudflare'],
    'gcp'             : ['aws'],
    'itil'            : ['company policy & governance', 'jira'],
    'information technology infrastructure library (itil)': ['company policy & governance'],
    'user experience design': ['figma', 'sketch'],
    'usability testing'     : ['figma', 'cypress', 'phpunit'],
    'jsp'                   : ['node.js', 'php'],
    'servlet'               : ['node.js', 'php'],
    'shell script'          : ['bash'],
    'subversion (svn)'      : ['svn', 'git'],
}


# ════════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════════

def parse_required_years(exp_str: str) -> int:
    """Parse '5 years or more' → 5, returning 0 if unparseable."""
    match = re.search(r'(\d+)', exp_str or '')
    return int(match.group(1)) if match else 0


def extract_job_terms(job_data: dict) -> list[tuple[str, str, int]]:
    """
    Flatten all skill terms from a job JSON into (term, source_section, weight) tuples.
    Sections with weight=0 (e.g. benefits) are skipped.
    """
    terms: list[tuple[str, str, int]] = []
    job_posting = job_data.get('job_posting', {}) or {}

    for section, items_or_dict in job_posting.items():
        weight = SECTION_WEIGHTS.get(section, 1)
        if weight == 0:
            continue

        if isinstance(items_or_dict, dict):
            for subsection, items in items_or_dict.items():
                if isinstance(items, list):
                    for item in items:
                        if item and isinstance(item, str):
                            terms.append((item.lower().strip(), f'{section}.{subsection}', weight))
        elif isinstance(items_or_dict, list):
            for item in items_or_dict:
                if item and isinstance(item, str):
                    terms.append((item.lower().strip(), section, weight))

    for _facet_id, skill_data in job_data.get('required_skills', {}).items():
        if isinstance(skill_data, dict) and (name := skill_data.get('facet_name')):
            terms.append((name.lower().strip(), 'required_skills', 3))

    for _facet_id, skill_data in job_data.get('additional_skills', {}).items():
        if isinstance(skill_data, dict) and (name := skill_data.get('facet_name')):
            terms.append((name.lower().strip(), 'additional_skills', 2))

    return terms


def resolve_to_facet(term: str, facet_lookup: dict) -> tuple[dict | None, bool]:
    """
    Resolve a job term to a facet entry.

    Returns:
        (facet_entry, is_adjacent_only)
        - facet_entry is None when no direct match exists.
        - is_adjacent_only is True when we hold a related skill but not this exact one.
    """
    term_lower = term.lower().strip()

    if term_lower in facet_lookup:
        return facet_lookup[term_lower], False

    aliased = ALIASES.get(term_lower, '').lower()
    if aliased and aliased in facet_lookup:
        return facet_lookup[aliased], False

    if len(term_lower) > 4:
        for fname, entry in facet_lookup.items():
            if term_lower in fname or fname in term_lower:
                return entry, False

    for adj_name in ADJACENCY_MAP.get(term_lower, []):
        if facet_lookup.get(adj_name, {}).get('proficiency'):
            return None, True

    return None, False


def compute_content_tag(
    facet: dict | None,
    is_adjacent: bool,
    section_weight: int,
    job_required_years: int,
    mention_count: int,
) -> tuple[str, float]:
    """
    Assign a content tag and compute a ranking score.

    Returns:
        (tag, score)
    """
    if facet is None:
        return ('HARD_GAP', 0.0)

    confidence    = facet.get('confidence_level') or 0
    years         = facet.get('years_of_experience') or 0
    proficiency   = facet.get('proficiency') or 'novice'
    last_used_str = facet.get('last_used') or ''
    facet_type    = facet.get('facet_type') or 'hands_on_skill'
    type_weight   = FACET_TYPE_WEIGHTS.get(facet_type, 0.7)

    stale = False
    if last_used_str:
        try:
            stale = (CURRENT_YEAR - int(last_used_str.split('-')[0])) >= STALE_YEAR_THRESHOLD
        except ValueError:
            pass

    prof_rank = {'novice': 1, 'beginner': 2, 'intermediate': 3, 'advanced': 4, 'expert': 5}.get(proficiency, 1)

    score = (
        (confidence / 10.0)         * 0.35 +
        (prof_rank  / 5.0)          * 0.30 +
        (min(years, 15) / 15.0)     * 0.20 +
        (mention_count / 5.0)       * 0.10 +
        (section_weight / 3.0)      * 0.05
    ) * type_weight

    if is_adjacent:
        score *= 0.65
        return ('GAP_ADJACENCY', round(score, 4))

    if stale:
        return ('UNTESTED_CLAIM', round(score, 4))

    if confidence >= LEAD_CONFIDENCE_MIN and prof_rank >= 4 and years >= job_required_years * LEAD_YEARS_MULTIPLIER:
        return ('LEAD_STRENGTH', round(score, 4))

    if confidence >= 7 and prof_rank >= 3:
        return ('SOLID_MATCH', round(score, 4))

    if confidence <= PARTIAL_CONFIDENCE_MAX or prof_rank <= 2:
        return ('PARTIAL_MATCH', round(score, 4))

    return ('SOLID_MATCH', round(score, 4))


# ════════════════════════════════════════════════════════════════════════════════
# MAIN REPORT BUILDER
# ════════════════════════════════════════════════════════════════════════════════

def build_correlation_report(job_data: dict, facet_lookup: dict) -> dict:
    """
    Build a full correlation report comparing a job posting against your facet lookup.

    Args:
        job_data:     Parsed job posting JSON.
        facet_lookup: Enriched facet dict keyed by lowercase facet_name.

    Returns:
        Correlation report dict ready for JSON serialisation.
    """
    job_posting = job_data.get('job_posting', job_data)
    job_required_years = parse_required_years(
        job_posting.get('overview', {}).get('experience', '0')
    )

    terms = extract_job_terms(job_data)

    facet_mention_counts:      dict[str, int]       = {}
    facet_section_weights:     dict[str, int]       = {}
    facet_adjacency_available: dict[str, bool]      = {}
    facet_sources:             dict[str, list[str]] = {}
    facet_by_term:             dict[str, dict]      = {}

    # First pass: resolve and aggregate
    for term, section, weight in terms:
        entry, has_adjacent = resolve_to_facet(term, facet_lookup)

        if entry is not None:
            fname = entry['facet_name'].lower()
            facet_mention_counts[fname]  = facet_mention_counts.get(fname, 0) + 1
            facet_section_weights[fname] = max(facet_section_weights.get(fname, 0), weight)
            facet_adjacency_available.setdefault(fname, False)
            facet_sources.setdefault(fname, [])
            if section not in facet_sources[fname]:
                facet_sources[fname].append(section)
            facet_by_term[fname] = entry

        elif has_adjacent:
            facet_mention_counts[term]  = facet_mention_counts.get(term, 0) + 1
            #!/usr/bin/env python3
            """Compatibility shim — forwards to data_processing/py_skill_job_correlator.py"""

            import os
            import sys

            HERE = os.path.dirname(os.path.realpath(__file__))
            NEW = os.path.join(HERE, 'data_processing', 'py_skill_job_correlator.py')
            if not os.path.exists(NEW):
                print(f"Error: relocated correlator not found at {NEW}")
                sys.exit(1)

            os.execv(sys.executable, [sys.executable, NEW] + sys.argv[1:])
            hard_gaps.append({'term': term, 'source_section': section})
