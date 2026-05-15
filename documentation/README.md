---
project_name: Resume Machine
title: Resume Machine
description: Pipeline architecture, components, configuration, and operating commands for Resume Machine.
last_updated: 2026-05-15
cleardoc_version: 2.3.0
keywords: [resume-machine, pipeline, commands, configuration, components, src]
---

# Resume Machine

An automated resume generation pipeline that analyzes job postings, correlates them against your skills inventory, and produces targeted, domain-aware PDF resumes.

---

## Overview

Resume Machine removes the manual work from tailoring resumes. It scrapes job postings, matches them against your skills, infers the most relevant domain (fullstack, backend, devops, etc.), selects the appropriate resume template, and exports a polished PDF — all from a single command.

```
╔══════════════════════════════════════════════════════════════════════════════════╗
║  DATA SOURCES                          RENDERED SECTIONS                        ║
╠══════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║  ┌─────────────────────┐   ┌──────────────────────────────────────────────────┐ ║
║  │ resume.source.json  │   │  PAGE 1 — COVER LETTER                           │ ║
║  │  basics.name        │──▶│  ┌─────────────────────────────────────────────┐ │ ║
║  │  basics.email       │   │  │ [name]                          cl-name      │ │ ║
║  │  basics.phone       │──▶│  │ email · phone · city, region    cl-contact   │ │ ║
║  │  basics.location    │   │  └─────────────────────────────────────────────┘ │ ║
║  └─────────────────────┘   │  ┌─────────────────────────────────────────────┐ │ ║
║                             │  │ May 13, 2026               cl-date (runtime)│ │ ║
║  ┌─────────────────────┐   │  └─────────────────────────────────────────────┘ │ ║
║  │ *_resume_*.json     │   │  ┌─────────────────────────────────────────────┐ │ ║
║  │  metadata.employer  │──▶│  │ [Employer Name]             cl-recipient     │ │ ║
║  └─────────────────────┘   │  └─────────────────────────────────────────────┘ │ ║
║                             │                                                  │ ║
║  ┌─────────────────────┐   │  ┌─────────────────────────────────────────────┐ │ ║
║  │ *_letter_*.json     │   │  │ Dear Hiring Team at {employer}…  cl-opening  │ │ ║
║  │  opening            │──▶│  │                                              │ │ ║
║  │  (from              │   │  │ [value proposition sentence]   cl-value      │ │ ║
║  │  opening_template   │   │  │                                              │ │ ║
║  │  + employer sub)    │   │  │  • highlight 1               cl-experience   │ │ ║
║  │  value_proposition  │──▶│  │  • highlight 2                    (up to 5)  │ │ ║
║  │  relevant_experience│──▶│  │  • highlight 3                              │ │ ║
║  │  closing            │──▶│  │                                              │ │ ║
║  │  (from              │   │  │ I would welcome the opportunity… cl-closing  │ │ ║
║  │  closing_template   │   │  └─────────────────────────────────────────────┘ │ ║
║  │  + employer sub)    │   └──────────────────────────────────────────────────┘ ║
║  └─────────────────────┘                                                        ║
║         ▲                  ┌──────────────────────────────────────────────────┐ ║
║         │ built by         │  PAGE 2 — RESUME                                 │ ║
║  ┌──────┴──────────────┐   │  ┌─────────────────────────────────────────────┐ │ ║
║  │cover-letter.source  │   │  │ [Name]                      r-name           │ │ ║
║  │.json                │   │  │ [basics.label OR job_title] r-role           │ │ ║
║  │  opening_template   │   │  │ email · phone · city        r-contact        │ │ ║
║  │  closing_template   │   │  └─────────────────────────────────────────────┘ │ ║
║  └─────────────────────┘   │                                                  │ ║
║                             │  ┌─────────────────────────────────────────────┐ │ ║
║  ┌─────────────────────┐   │  │ ABSTRACT                                     │ │ ║
║  │ resume.source.json  │   │  │ [summary[0].value narrative ¶] r-abstract    │ │ ║
║  │  basics.summary     │──▶│  │  ▸ highlight 1              r-summary        │ │ ║
║  │    [0].value        │   │  │  ▸ highlight 2              (up to 4,        │ │ ║
║  │                     │   │  │  ▸ highlight 3               from corr.)     │ │ ║
║  │ *_resume_*.json     │   │  │  ▸ highlight 4                               │ │ ║
║  │  highlights[]       │──▶│  └─────────────────────────────────────────────┘ │ ║
║  └─────────────────────┘   │                                                  │ ║
║                             │  ┌─────────────────────────────────────────────┐ │ ║
║  ┌─────────────────────┐   │  │ AREAS OF EXPERTISE                           │ │ ║
║  │ resume.source.json  │   │  │ Full-Stack Dev · PHP & JS · CMS · …          │ │ ║
║  │  interests[0]       │──▶│  │                              r-expertise      │ │ ║
║  │  .keywords[]        │   │  └─────────────────────────────────────────────┘ │ ║
║  └─────────────────────┘   │                                                  │ ║
║                             │  ┌─────────────────────────────────────────────┐ │ ║
║  ┌─────────────────────┐   │  │ EXPERIENCE                                   │ │ ║
║  │ resume.source.json  │   │  │ Company ──────────────────────────── 20XX    │ │ ║
║  │  work[].name        │──▶│  │ Position (italic)                            │ │ ║
║  │  work[].position    │   │  │ Summary paragraph                            │ │ ║
║  │  work[].startDate   │   │  │  • highlight                  r-work         │ │ ║
║  │  work[].endDate     │   │  │  • highlight                                 │ │ ║
║  │  work[].summary     │   │  └─────────────────────────────────────────────┘ │ ║
║  │  work[].highlights  │   │                                                  │ ║
║  └─────────────────────┘   │  ┌─────────────────────────────────────────────┐ │ ║
║                             │  │ SKILLS  (priority groups first per domain)  │ │ ║
║  ┌─────────────────────┐   │  │ Languages & Frameworks (accent if priority)  │ │ ║
║  │ resume.source.json  │   │  │ PHP · JS · Node.js · React · …              │ │ ║
║  │  skills[].name      │──▶│  │ DevOps, Infrastructure & Development        │ │ ║
║  │  skills[].keywords  │   │  │ Docker · AWS · CI/CD · …      r-skills       │ │ ║
║  │                     │   │  └─────────────────────────────────────────────┘ │ ║
║  │ *_resume_*.json     │   │          ▲                                       │ ║
║  │  domain             │──▶│  sort order decided by domain                   │ ║
║  └─────────────────────┘   │                                                  │ ║
║                             │  ┌─────────────────────────────────────────────┐ │ ║
║  ┌─────────────────────┐   │  │ OPEN SOURCE & COMMUNITY LEADERSHIP           │ │ ║
║  │ resume.source.json  │   │  │ Project Name  Creator, Maintainer            │ │ ║
║  │  projects[]         │──▶│  │ Description · link           r-community     │ │ ║
║  │  volunteer[]        │──▶│  │ Organization, Role  2012–2014                │ │ ║
║  └─────────────────────┘   │  └─────────────────────────────────────────────┘ │ ║
║                             │                                                  │ ║
║  ┌─────────────────────┐   │  ┌─────────────────────────────────────────────┐ │ ║
║  │ resume.source.json  │   │  │ EDUCATION                                    │ │ ║
║  │  education[]        │──▶│  │ Institution — Degree, Area    r-education    │ │ ║
║  └─────────────────────┘   │  └─────────────────────────────────────────────┘ │ ║
║                             │                                                  │ ║
║  ┌─────────────────────┐   │  ┌─────────────────────────────────────────────┐ │ ║
║  │ resume.source.json  │   │  │ jamesvaleii.com · linkedin.com/… · github… │ │ ║
║  │  basics.url         │──▶│  │                               r-footer       │ │ ║
║  │  basics.profiles[]  │   │  └─────────────────────────────────────────────┘ │ ║
║  └─────────────────────┘   └──────────────────────────────────────────────────┘ ║
╚══════════════════════════════════════════════════════════════════════════════════╝

  KEY
  ──────────────────────────────────────────────────────────────────────────────
  resume.source.json   static candidate data, edited manually, never overwritten
  *_resume_*.json      per-job correlation output, written by process.py
  *_letter_*.json      per-job cover letter output, written by process.py
  cover-letter.source  templates with {employer}/{job_title} placeholders
  domain               one of: ai · backend · database · devops · frontend
                               fullstack · manager  (controls skill sort order)
  highlights[]         drawn from the matched role-based-template (ai.json etc.)
```

---

## Configuration System

Resume Machine reads all settings from `config/config.yaml`. Override candidate name at runtime with the `--name` flag.

### Configuration File

`config/config.yaml`:

```yaml
candidate_name: "james-valeii"
job-listings_dir: data/job-listings
skills_catalog_path: data/source/skills-catalog.json
skills_index_path: data/source/skills-index.json
resume_source_path: data/source/resume.source.json
letter_source_path: data/source/letter.source.json
reasoning_dir: data/source/reasoning
role_templates_dir: data/domains
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

Start the UX server (defaults to port 8080):

```bash
python -m src.api.serve
python -m src.api.serve --port 9000  # custom port
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
  "highlight_1": "<strong>E2E feature ownership</strong>; database → API → UI...",
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

Domain templates live in `data/domains/`. Each domain has three files:

| Domain | Resume template | Letter template | Interests template |
|--------|----------------|-----------------|--------------------|
| `ai` | `ai-resume.json` | `ai-letter.json` | `ai-interests.json` |
| `backend` | `backend-resume.json` | `backend-letter.json` | `backend-interests.json` |
| `database` | `database-resume.json` | `database-letter.json` | `database-interests.json` |
| `devops` | `devops-resume.json` | `devops-letter.json` | `devops-interests.json` |
| `frontend` | `frontend-resume.json` | `frontend-letter.json` | `frontend-interests.json` |
| `fullstack` | `fullstack-resume.json` | `fullstack-letter.json` | `fullstack-interests.json` |
| `manager` | `manager-resume.json` | `manager-letter.json` | `manager-interests.json` |

Shared letter and resume source templates also live here: `letter.source.json`, `resume.source.json`.

---

## Extending the Pipeline

### Add a new domain

1. Create three files in `data/domains/`: `your_domain-resume.json`, `your_domain-letter.json`, `your_domain-interests.json`. The resume template must include a `domain` field set to `"your_domain"` and a `keywords` array listing trigger terms.
2. The adapter (`src/models/py_adapter_correlator_to_template.py`) loads all `*-resume.json` templates at startup and scores each domain by keyword overlap with the correlation terms — no code changes required.

### Extend the skills inventory

Add or update facets directly in `data/skills-index.json` under the `facet_catalog` array. The correlator reads facets via `_build_facet_lookup()` on each run.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'src'` | Run from the project root: `cd /path/to/0-career-cv && python -m src.api.serve` |
| "Adapter output is not valid JSON" | Validate the correlation file: `cat correlation-*.json \| jq .` |
| "Correlator unavailable; falling back to manual" | Confirm job JSON exists: `find data/job-listings -name "*.json"` |
| All jobs map to `fullstack` domain | Review keyword coverage in `data/domains/`; inspect correlation scores in output JSON |
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
| `documentation/README.md` | This document — pipeline architecture, components, configuration, and commands |
| `documentation/abstract.md` | Abstract and design intent |
| `documentation/composition.md` | Composition engine usage |
| `documentation/roadmap/roadmap.md` | Project roadmap and sprint history |
