#!/usr/bin/env python3
"""
Adapter: correlation data → role-based template selection.

Reads a correlation_*.json produced by py_skill_job_correlator.py, infers the
best-fit domain, and emits a JSON object suitable for merging into
resume.unique-data.json.

Usage:
  python py_adapter_correlator_to_template.py <correlation_json_path>

Output:
  JSON to stdout — pipe into jq or capture in a shell variable.

Example:
  template=$(python resume-machine/scripts/py_adapter_correlator_to_template.py \\
    jobbankjobs/2026/04/05/correlation_software_developer_kanata.json)
  jq --argjson t "$template" '. += $t' resume.unique-data.json
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ════════════════════════════════════════════════════════════════════════════════
# DOMAIN PATTERNS
# ════════════════════════════════════════════════════════════════════════════════

DOMAIN_PATTERNS: Dict[str, Dict] = {
    'devops': {
        'keywords': {'docker', 'kubernetes', 'terraform', 'ansible', 'ci/cd',
                     'aws', 'azure', 'gcp', 'prometheus', 'grafana', 'jenkins'},
        'facet_types': {'hands_on_tool', 'hands_on_platform'},
        'highlights': [
            "<strong>Containerization & orchestration</strong>; Docker, Kubernetes, Helm, automated rollouts.",
            "<strong>Infrastructure-as-code & automation</strong>; Terraform, Ansible, orchestrated deployments.",
            "<strong>Observability & monitoring</strong>; Prometheus, Grafana, alerting, tracing, runbooks.",
            "<strong>CI/CD pipelines</strong>; automated testing, multi-stage builds, deployment strategies.",
            "<strong>Cloud platform expertise</strong>; AWS/Azure/GCP—cost optimization, autoscaling, security.",
            "<strong>Reliability engineering</strong>; SRE practices, incident response, capacity planning.",
        ],
    },
    'backend': {
        'keywords': {'node.js', 'django', 'flask', 'fastapi', 'spring boot',
                     '.net', 'express', 'rest api', 'graphql', 'microservices'},
        'facet_types': {'hands_on_language', 'hands_on_framework'},
        'highlights': [
            "<strong>RESTful & async API design</strong>; high-throughput, event-driven architectures.",
            "<strong>Database optimization</strong>; query design, indexing, caching strategies (Redis, Varnish).",
            "<strong>Microservices architecture</strong>; service boundaries, async messaging, fault tolerance.",
            "<strong>Framework expertise</strong>; production-grade server patterns, middleware, authentication.",
            "<strong>Performance & scalability</strong>; load testing, profiling, horizontal scaling.",
            "<strong>Software testing & quality</strong>; unit/integration tests, TDD, code coverage.",
        ],
    },
    'frontend': {
        'keywords': {'react', 'angular', 'vue', 'html5', 'css/sass',
                     'typescript', 'webpack', 'next.js'},
        'facet_types': {'hands_on_framework', 'hands_on_language'},
        'highlights': [
            "<strong>Component-driven UI architecture</strong>; reusable, testable React/Vue/Angular components.",
            "<strong>State management & data flow</strong>; Redux, Context, MobX—predictable, debuggable patterns.",
            "<strong>Performance optimization</strong>; code splitting, lazy loading, bundle analysis, Core Web Vitals.",
            "<strong>Responsive & accessible design</strong>; CSS Grid/Flexbox, WCAG compliance, mobile-first.",
            "<strong>Build tooling & bundling</strong>; Webpack, Vite, esbuild—production-ready pipelines.",
            "<strong>Testing & QA</strong>; Jest, Cypress, end-to-end scenarios, visual regression.",
        ],
    },
    'fullstack': {
        'keywords': {'javascript', 'typescript', 'node.js', 'react', 'next.js',
                     'sql/mysql', 'mongodb', 'rest api'},
        'facet_types': {'hands_on_language', 'hands_on_framework'},
        'highlights': [
            "<strong>End-to-end feature ownership</strong>; database → API → UI, holistic optimization.",
            "<strong>Modern JavaScript ecosystems</strong>; Node.js servers, React clients, shared tooling.",
            "<strong>Database design & optimization</strong>; schema modeling, migrations, query optimization.",
            "<strong>API design & integration</strong>; RESTful/GraphQL endpoints, SDKs, third-party services.",
            "<strong>DevOps & deployment</strong>; containerization, CI/CD, monitoring, scaling.",
            "<strong>Testing across layers</strong>; unit, integration, E2E—full-stack confidence.",
        ],
    },
    'ml_ai': {
        'keywords': {'python', 'tensorflow', 'pytorch', 'scikit-learn',
                     'pandas', 'jupyter', 'data science', 'machine learning'},
        'facet_types': {'hands_on_language', 'strategic_domain'},
        'highlights': [
            "<strong>Model training & evaluation</strong>; hyperparameter tuning, cross-validation, performance metrics.",
            "<strong>Feature engineering & preprocessing</strong>; data pipelines, normalization, dimensionality reduction.",
            "<strong>Deep learning architectures</strong>; CNNs, RNNs, transformers—modern frameworks, deployment.",
            "<strong>Data analysis & visualization</strong>; pandas, matplotlib, exploratory analysis for insights.",
            "<strong>MLOps & production</strong>; model versioning, A/B testing, monitoring, retraining pipelines.",
            "<strong>Statistical rigor</strong>; hypothesis testing, experiment design, statistical significance.",
        ],
    },
    'database': {
        'keywords': {'sql/mysql', 'postgresql', 'mongodb', 'elasticsearch',
                     'redis', 'cassandra', 'database'},
        'facet_types': {'hands_on_tool'},
        'highlights': [
            "<strong>Relational database design</strong>; schema modeling, normalization, indexes, constraints.",
            "<strong>Query optimization & performance</strong>; execution plans, indexing strategies, query tuning.",
            "<strong>NoSQL expertise</strong>; document stores, time-series DBs—trade-offs, consistency models.",
            "<strong>Replication & high availability</strong>; clustering, failover, backup strategies.",
            "<strong>Database administration</strong>; user management, security, monitoring, upgrades.",
            "<strong>ETL & data pipelines</strong>; data loading, transformation, integration across systems.",
        ],
    },
    'manager': {
        'keywords': {'scrum', 'agile', 'project management', 'mentoring',
                     'leadership', 'team', 'jira'},
        'facet_types': {'leadership_soft_skill'},
        'highlights': [
            "<strong>Agile team leadership</strong>; sprint planning, retrospectives, velocity forecasting.",
            "<strong>Mentoring & growth</strong>; code review, knowledge transfer, career development.",
            "<strong>Cross-functional collaboration</strong>; product, design, ops—alignment, communication.",
            "<strong>Risk & conflict management</strong>; escalation, decision-making, stakeholder engagement.",
            "<strong>Technical roadmapping</strong>; architecture decisions, tech debt prioritization.",
            "<strong>Team scaling & hiring</strong>; recruitment, onboarding, culture, retention.",
        ],
    },
}

# Default domain when no pattern scores above zero.
DEFAULT_DOMAIN = 'fullstack'


# ════════════════════════════════════════════════════════════════════════════════
# CORE LOGIC
# ════════════════════════════════════════════════════════════════════════════════

def load_correlation(path: str) -> Dict:
    with open(path) as f:
        return json.load(f)


def identify_domain(correlations: List[Dict]) -> str:
    """
    Score each domain by counting LEAD_STRENGTH facet matches against its
    keyword set, then return the highest-scoring domain.

    Uses sets for O(1) keyword lookup and avoids double-counting a facet that
    matches multiple domain keyword lists (each facet contributes at most 1
    point per domain).
    """
    lead_facets = {
        c['facet_name'].lower()
        for c in correlations
        if c.get('content_tag') == 'LEAD_STRENGTH'
    }

    scores: Dict[str, int] = {
        domain: sum(1 for facet in lead_facets if facet in pattern['keywords'])
        for domain, pattern in DOMAIN_PATTERNS.items()
    }

    best_score = max(scores.values(), default=0)
    if best_score == 0:
        return DEFAULT_DOMAIN

    return max(scores, key=scores.get)


def extract_featured_languages(correlations: List[Dict], limit: int = 3) -> Optional[str]:
    """
    Return a comma-separated string of the top LEAD_STRENGTH hands-on languages,
    or None if none are found.
    """
    languages = [
        c['facet_name']
        for c in correlations
        if c.get('content_tag') == 'LEAD_STRENGTH'
        and c.get('facet_type') == 'hands_on_language'
    ]
    return ', '.join(languages[:limit]) if languages else None


def generate_template(correlation_data: Dict) -> Dict:
    """
    Build a template dict from correlation data.

    Returns:
        Dict ready for merging into resume.unique-data.json.
    """
    correlations = correlation_data.get('correlations', [])
    metadata     = correlation_data.get('metadata', {})

    domain             = identify_domain(correlations)
    featured_languages = extract_featured_languages(correlations)
    highlights         = DOMAIN_PATTERNS[domain]['highlights']

    template: Dict = {
        'domain_inference': domain,
        'job_title':        metadata.get('job_title', ''),
    }

    if featured_languages:
        template['featured_languages'] = featured_languages

    for i, highlight in enumerate(highlights[:6], 1):
        template[f'highlight_{i}'] = highlight

    return template


# ════════════════════════════════════════════════════════════════════════════════
# CLI
# ════════════════════════════════════════════════════════════════════════════════

def main() -> None:
    if len(sys.argv) < 2:
        print(
            'Usage: python py_adapter_correlator_to_template.py <correlation_json_path>',
            file=sys.stderr,
        )
        sys.exit(1)

    correlation_path = sys.argv[1]

    try:
        correlation_data = load_correlation(correlation_path)
        template = generate_template(correlation_data)
        print(json.dumps(template, indent=2))
    except FileNotFoundError:
        print(f'ERROR: File not found: {correlation_path}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({'error': str(e), 'correlation_path': correlation_path}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
