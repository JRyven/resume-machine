---
project_name: Resume Machine
title: Resume Machine
description: Pipeline architecture, components, configuration, and operating commands for Resume Machine.
last_updated: 2026-05-12
cleardoc_version: 2.3.0
keywords: [resume-machine, pipeline, commands, configuration, components, src]
---

# Resume Machine

An automated resume generation pipeline that analyzes job postings, correlates them against your skills inventory, and produces targeted, domain-aware PDF resumes.

---

## Overview

Resume Machine removes the manual work from tailoring resumes. It scrapes job postings, matches them against your skills, infers the most relevant domain (fullstack, backend, devops, etc.), selects the appropriate resume template, and exports a polished PDF — all from a single command.

```
RESUME MACHINE — PIPELINE MAP
══════════════════════════════════════════════════════════════

INPUT                         PROCESSING                      DATA / CONFIG
─────                         ────────────                    ───────────

[Job Bank HTML files]
        │
        ▼
                    [src/data/py_extract_jobs.py]
                    HTML → structured job JSON
                                │
                                ▼
                    [job JSON files]           ----╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                                │             ╎ data/skills-index.json     ╎
                                │╌╌╌╌╌╌╌╌╌╌╌╌╎ (skills inventory)         ╎
                                │              ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                                ▼
                    [src/data/py_skill_job_correlator.py]
                    Skill–job correlation + tag assignment
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
         [correlation-*.json]       [letter-*.json]
          always overwritten         written once
                    └───────────┬───────────┘
                                │
                                ▼
                    [src/models/py_adapter_correlator_to_template.py]
                    Domain inference         ----╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
                                       ╌╌╌╌╌╌╌╎ data/role-based-templates/ ╎
                                               ╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

──────────────────────────────────────────────────────────────
ORCHESTRATION
  scripts/process.py          ← batch orchestrator (--dir / --file)
  python -m src.api.serve     ← local HTTP server (resume selection UX)
──────────────────────────────────────────────────────────────
LEGEND
  [name]        script or orchestrator
  ╎ name ╎      data / config file (side input)
  ──────        main flow
  ╌╌╌╌╌╌        supporting / fallback input
──────────────────────────────────────────────────────────────
```

---

## Configuration System

Resume Machine reads all settings from `config/config.yaml`. Override candidate name at runtime with the `--name` flag.

### Configuration File

`config/config.yaml`:

```yaml
candidate_name: "james-valeii"
job-listings_dir: data/job-listings
skills_index_path: data/skills-index.json
resume_source_path: data/resume.source.json
role_templates_dir: data/role-based-templates
log_level: info
```

### Usage Examples

Process all job JSON files in a day directory:

```bash
python scripts/process.py --dir data/job-listings/2026/05/01
```

Process a single job JSON file:

```bash
python scripts/process.py --file data/job-listings/2026/05/01/sample.json
```

Override candidate name:

```bash
python scripts/process.py --dir data/job-listings/2026/05/01 --name "Jane Doe"
```

Dry-run preview:

```bash
python scripts/process.py --dir data/job-listings/2026/05/01 --dry-run
```

Start the UX server:

```bash
python -m src.api.serve
python -m src.api.serve --port 8080
```

---

## Components

### Job Extractor (`src/data/py_extract_jobs.py`)

Parses Job Bank Canada HTML files using BeautifulSoup4 + lxml. Extracts structured job data: title, employer, location, salary, employment type, required skills, additional skills, responsibilities, and overview. Writes one job JSON file per HTML input.

**Usage:**

```bash
python -m src.data.py_extract_jobs <input_dir>
```

```bash
python -m src.data.py_extract_jobs /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv/data/job-listings/2026/05
```

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
| `ai` | Python, TensorFlow, PyTorch, scikit-learn |
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
python -m src.models.py_adapter_correlator_to_template \
  data/job-listings/2026/05/01/correlation_software_developer_kanata.json
```

---

### Process Orchestrator (`scripts/process.py`)

Batch orchestrator CLI. Processes all job JSON files in a directory or a single file through the correlator. Must run inside the project `.venv`.

**Flags:**

| Flag | Description |
|------|-------------|
| `--dir DIR` | Process all job JSONs in a day-level directory |
| `--file FILE` | Process a single job JSON |
| `--dry-run` | Print output paths without writing files |
| `--name NAME` | Override candidate name (slugified before use in paths) |

**Examples:**

```bash
# Process all jobs for a day
python scripts/process.py --dir data/job-listings/2026/05/01

# Process a single job
python scripts/process.py --file data/job-listings/2026/05/01/sample.json

# Dry-run preview
python scripts/process.py --dir data/job-listings/2026/05/01 --dry-run
```

---

## Template Files

Role-based templates live in `data/role-based-templates/`:

- `fullstack.json`
- `backend.json`
- `frontend.json`
- `devops.json`
- `database.json`
- `ai.json`
- `manager.json`

---

## Extending the Pipeline

### Add a new domain

1. Create a new JSON file in `data/role-based-templates/your_domain.json` with a `domain` field set to `"your_domain"` and a `keywords` array listing trigger terms.
2. The adapter (`src/models/py_adapter_correlator_to_template.py`) loads all templates at startup and scores each domain by keyword overlap with the correlation terms — no code changes required.

### Extend the skills inventory

Add or update facets directly in `data/skills-index.json` under the `facet_catalog` array. The correlator reads facets via `_build_facet_lookup()` on each run.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'src'` | Run from the project root: `cd /path/to/0-career-cv && python -m src.api.serve` |
| "Adapter output is not valid JSON" | Validate the correlation file: `cat correlation-*.json \| jq .` |
| "Correlator unavailable; falling back to manual" | Confirm job JSON exists: `find data/job-listings -name "*.json"` |
| All jobs map to `fullstack` domain | Review keyword coverage in `data/role-based-templates/`; inspect correlation scores in output JSON |
| `resumed` not found | Ensure the `resumed` CLI is installed and available on `PATH` |
| Domain inference incorrect | Add or update keywords in the relevant template in `data/role-based-templates/` |

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
