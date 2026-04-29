# Resume Machine

An automated resume generation pipeline that analyzes job postings, correlates them against your skills inventory, and produces targeted, domain-aware PDF resumes.

---

## Overview

Resume Machine removes the manual work from tailoring resumes. It scrapes job postings, matches them against your skills, infers the most relevant domain (fullstack, backend, devops, etc.), selects the appropriate resume template, and exports a polished PDF — all from a single command.

```
RESUME MACHINE — PIPELINE MAP
══════════════════════════════════════════════════════════════

INPUT                         PROCESSING                      DATA / CONFIG
─────                         ──────────                      ─────────────

[Job Bank HTML files]
        │
        ▼
                        [py_extract_jobs.py]
                                │
                                ▼
                        [resume-machine-queue.json]
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             [batch-process.sh]   [py_orchestrate_correlation_to_pdf.py]
              Multi-job runner     Single-job runner
                    │                       │
                    └───────────┬───────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
          [job_skill_analyzer.py]  [py_skill_job_correlator.py]
          Extract + match skills    Skill–job correlation
                    │                       │         ----╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                    │                       │        ╎ skills-index.json   ╎
                    │                       │╌╌╌╌╌╌╌╌╎ (skills inventory)  ╎
                    └───────────┬───────────┘         ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                                │
                                ▼
                      [correlation_*.json]
                       Per-job correlation output
                                │
                                ▼
                      [py_adapter_correlator_to_template.py]
                       Domain inference + highlights
                                │
                                ▼                       ----╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                      [resume.unique-data.json] ╌╌╌╌╌╌ ╎ resume.defaults.json   ╎
                       Merge target             ╌╌╌╌╌╌ ╎ (fallback template)    ╎
                                │                       ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌--╌╌
                                │               ╌╌╌╌╌╌╌╎ role-based-templates/  ╎
                                │╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╎ (domain template files)╎
                                │                        ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                    ┌───────────┴───────────┐
                    ▼                       ▼
            [compose_resume.py]       [preprocess-resume.js]
            YAML fragments → JSON     Variable substitution
                    └───────────┬───────────┘
                                ▼
                           [resume.json]
                                │
                                ▼
                           [resumed CLI] ← runtime dependency
                                │
                                ▼
                           [resume-*.pdf]
                            artifacts/

──────────────────────────────────────────────────────────────
LEGEND
  [name]        script or orchestrator
  ╎ name ╎      data / config file (side input)
  ──────        main flow
  ╌╌╌╌╌╌        supporting / fallback input
```

---

## Components

### Job Skill Analyzer (`job_skill_analyzer.py`)

A modular, three-tier skill resolution pipeline. Parses Job Bank Canada HTML files and matches extracted skills against your `skills-index.json` inventory.

**Resolution tiers:**

1. **Exact match** — normalized name lookup
2. **Alias table** — 201 entries mapping job posting terminology to canonical facet names (e.g. `spring boot` → `Spring / SpringBoot`, `k8s` → `Kubernetes`)
3. **Substring match** — conservative fallback for partial matches

**Usage:**

```bash
# Single job posting
python3 job_skill_analyzer.py 'path/to/job.html'

# Batch — processes all *.html in the configured directory
python3 job_skill_analyzer.py
```

**Programmatic API:**

```python
from job_skill_analyzer import analyze_job_posting, batch_analyze_job_postings

# Single job
result = analyze_job_posting('job.html', verbose=True)

# Batch with filtering
results = batch_analyze_job_postings(verbose=False)
high_match = [r for r in results if r['result']['report']['summary']['match_rate_pct'] > 10]
```

See `ANALYZER_USAGE_EXAMPLES.py` for 8 complete usage scenarios including gap analysis, custom reporting, and downstream data access.

---

### Correlation → Template Adapter (`py_adapter_correlator_to_template.py`)

Reads `correlation_*.json` output from the correlator, infers the best-fit resume domain, and generates domain-specific highlights.

**Supported domains:**

| Domain | Trigger Keywords |
|--------|-----------------|
| `fullstack` | JavaScript, Node.js, React, SQL |
| `backend` | Node, Django, Flask, FastAPI, REST |
| `frontend` | React, Angular, Vue, TypeScript |
| `devops` | Docker, Kubernetes, Terraform, Prometheus |
| `database` | SQL, MySQL, MongoDB, PostgreSQL |
| `ml_ai` | Python, TensorFlow, PyTorch, scikit-learn |
| `manager` | Scrum, Agile, mentoring, leadership |

**Output:**

```json
{
  "featured_languages": "PHP, BASH, JavaScript",
  "domain_inference": "fullstack",
  "job_title": "software developer",
  "highlight_1": "<strong>End-to-end feature ownership</strong>; database → API → UI...",
  "highlight_2": "...",
  ...
}
```

**Usage:**

```bash
python resume-machine/scripts/py_adapter_correlator_to_template.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json
```

---

### Batch Processor (`batch-process.sh`)

Orchestrates the full pipeline from queue to PDF. Version 2 adds automated template selection via the adapter.

**Flags:**

| Flag | Description |
|------|-------------|
| *(none)* | Interactive — shows adapter recommendation per job, prompts for acceptance |
| `--auto-template` | Non-interactive — accepts all adapter recommendations automatically |
| `--dry-run` | Preview mode — shows what would happen without generating PDFs |

**Examples:**

```bash
# Interactive run
./resume-machine/scripts/batch-process.sh

# Fully automated
./resume-machine/scripts/batch-process.sh --auto-template

# Preview only
./resume-machine/scripts/batch-process.sh --dry-run

# CI/CD
INPUT_DIR=jobbankjobs/2026/04/05 \
  ./resume-machine/scripts/batch-process.sh --auto-template
```

**Environment variables:**

```bash
INPUT_DIR=path/to/html   # Override default job HTML directory
SKIP_EXTRACT=true        # Skip HTML extraction, use existing queue.json
```

---

### Standalone Orchestrator (`py_orchestrate_correlation_to_pdf.py`)

End-to-end processing for a single job: correlation → template → `resume.json` → PDF.

```bash
# Generate PDF
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json

# Dry-run preview
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json \
  --dry-run
```

---

### Composition Engine (`compose_resume.py`, `build_resume.py`)

Assembles `resume.json` from modular YAML fragments using deep-merge rules: dicts merge, lists extend, scalars are overridden by fragments.

```bash
# Compose YAML fragments into JSON Resume
python scripts/compose_resume.py \
  --base content/base.yaml \
  --fragments content/fragments/experience/goop.yaml \
               content/fragments/skills/full-stack.yaml \
  -o build/resume.json \
  --validate schema/jsonresume-schema.json

# Build PDF (dry-run)
python scripts/build_resume.py \
  --base content/base.yaml \
  --role senior-engineer \
  --output-dir artifacts \
  --dry-run
```

> **Note:** `build_resume.py` writes a sidecar `resume.metadata.json` to avoid visible generation timestamps in the PDF body. The `resumed` CLI must be installed and on `PATH` for actual PDF export.

---

## Template Files

Role-based templates live in `resume-machine/role-based-templates/`:

- `resume.defaults.json` — fallback defaults
- `resume.fullstack.json`
- `resume.backend.json`
- `resume.frontend.json`
- `resume.devops.json`
- `resume.database.json`
- `resume.ml_ai.json`
- `resume.manager.json`

---

## Extending the Pipeline

### Add a new domain

1. Add an entry to `DOMAIN_PATTERNS` in `py_adapter_correlator_to_template.py`:

```python
DOMAIN_PATTERNS = {
    'your_domain': {
        'keywords': [...],
        'facet_types': [...],
        'highlights': [...]
    }
}
```

2. Create a matching template: `resume-machine/role-based-templates/resume.your_domain.json`

### Add alias mappings

Run the batch analyzer to find high-frequency unmatched skills, then add them to the `ALIASES` dict in `job_skill_analyzer.py`:

```python
ALIASES: Dict[str, str] = {
    'your raw term': 'Canonical Facet Name',
    ...
}
```

### Add a new resolution tier (e.g. fuzzy matching)

```python
def resolve_facet(raw_skill: str, index: Dict) -> Optional[Dict]:
    # ... existing tiers 1-3 ...
    # Tier 4: fuzzy match
    if not result:
        best = fuzzy_match_candidate(raw_skill, index['facet_by_name'])
        if best and best[1] > 0.85:
            return best[0]
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Adapter output is not valid JSON" | Validate the correlation file: `cat correlation_*.json \| jq .` |
| "Correlator unavailable; falling back to manual" | Confirm job JSON exists: `find jobbankjobs -name "*.json"` |
| All PDFs use `default` template | Check `DOMAIN_PATTERNS` keyword coverage; add `set -x` in the script to debug |
| `resumed` not found | Ensure the `resumed` CLI is installed and available on `PATH` |
| Domain inference incorrect | Extend `DOMAIN_PATTERNS` keywords or review correlation scores |

---

## Performance

| Stage | Time |
|-------|------|
| Index loading | ~10 ms (one-time) |
| HTML parsing | ~50 ms per file |
| Skill matching | ~5 ms per report |
| Correlator | 2–5 s per job |
| Adapter | < 1 s per correlation |
| Batch (11 files) | ~1 s (analysis) + ~5–7 min (with correlator + adapter) |
| PDF generation | ~200–300 per minute |

---

## Documentation

| File | Description |
|------|-------------|
| `ANALYZER.md` | Analyzer pipeline architecture and API reference |
| `ANALYZER_USAGE_EXAMPLES.py` | 8 working usage examples |
| `ADAPTER_README.md` | Adapter architecture, domains, and data flow |
| `BATCH_PROCESS_V2_GUIDE.md` | Complete batch processor v2 reference |
| `BATCH_PROCESS_V2_QUICKSTART.md` | 3-minute setup guide |
| `INTEGRATION_GUIDE.sh` | Code snippets for custom integration |
| `composition.md` | Composition engine usage |
