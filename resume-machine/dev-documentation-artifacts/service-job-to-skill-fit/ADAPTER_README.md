# Adapter: Correlation → Template Pipeline

**Purpose:** Bridge skill-job correlation analysis with resume template selection, automating what was previously manual template assignment during batch processing.

## Architecture

```
py_extract_jobs.py
  ↓ [HTML → JSON]
resume-machine-queue.json
  ↓ [batch-process.sh or py_skill_job_correlator.py]
correlation_*.json
  ↓ [py_adapter_correlator_to_template.py ← NEW]
template data (JSON)
  ↓ [merge into resume.unique-data.json]
preprocess-resume.js
  ↓ [variable substitution]
resume.json
  ↓ [resumed CLI export]
artifacts/resume-*.pdf
```

## Components

### `py_adapter_correlator_to_template.py`

**Role:** Analyze correlation data → infer domain → generate template highlights

**Input:** `correlation_*.json` from `py_skill_job_correlator.py`

**Output:** JSON template object with:

- `featured_languages`: Top languages from LEAD_STRENGTH matches
- `domain_inference`: Best-fit domain (fullstack, backend, frontend, devops, database, ml_ai, manager)
- `highlight_1...6`: Domain-specific resume highlights tailored to job fit

**Domains & Patterns:**
| Domain | Keywords | Use Case |
|--------|----------|----------|
| `fullstack` | JavaScript, Node.js, React, SQL | Full-stack web apps |
| `backend` | Node, Django, Flask, FastAPI, REST | Server-side services |
| `frontend` | React, Angular, Vue, TypeScript | Client-side UI |
| `devops` | Docker, Kubernetes, Terraform, Prometheus | Infrastructure & reliability |
| `database` | SQL, MySQL, MongoDB, PostgreSQL | Data-intensive systems |
| `ml_ai` | Python, TensorFlow, PyTorch, scikit-learn | Machine learning |
| `manager` | Scrum, Agile, mentoring, leadership | Team leadership |

**Example:**

```bash
python resume-machine/scripts/py_adapter_correlator_to_template.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json

# Output:
{
  "featured_languages": "PHP, BASH, JavaScript",
  "domain_inference": "fullstack",
  "job_title": "software developer",
  "highlight_1": "<strong>End-to-end feature ownership</strong>; database → API → UI...",
  "highlight_2": "<strong>Modern JavaScript ecosystems</strong>; Node.js servers...",
  ...
}
```

### `py_orchestrate_correlation_to_pdf.py`

**Role:** End-to-end orchestration—correlation → template → resume.json → PDF

**Usage:**

```bash
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json

# Or dry-run to preview:
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json \
  --dry-run
```

## Integration Strategies

### Option A: Update `batch-process.sh`

Modify the batch processing script to invoke the adapter before template selection:

```bash
# After job extraction, for each queue entry:
# 1. Run correlator (if correlation doesn't exist)
correlation_file="jobbankjobs/${date}/correlation_${title_slug}.json"
if [ ! -f "$correlation_file" ]; then
  python resume-machine/scripts/py_skill_job_correlator.py "$job_json" > "$correlation_file"
fi

# 2. Run adapter to get template
template_json=$(python resume-machine/scripts/py_adapter_correlator_to_template.py "$correlation_file")

# 3. Merge into unique-data and continue as normal
jq --argjson tmpl "$template_json" '. += $tmpl' \
  resume-machine/role-based-templates/default/resume.unique-data.json > tmpfile && \
  mv tmpfile resume-machine/role-based-templates/default/resume.unique-data.json
```

### Option B: Standalone Orchestration

Use the orchestration script for single-job processing:

```bash
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json
```

### Option C: Custom Python Orchestration

Import the adapter module directly in custom workflow:

```python
from py_adapter_correlator_to_template import load_correlation, generate_template

correlation_data = load_correlation('correlation_*.json')
template = generate_template(correlation_data)
# Use template in resume generation...
```

## Data Flow Example

**Input:** Correlation for "Software Developer" role

```json
{
  "metadata": { "job_title": "software developer", ... },
  "summary": { "tag_distribution": { "LEAD_STRENGTH": 4, ... } },
  "correlations": [
    { "facet_name": "PHP", "facet_type": "hands_on_language", "content_tag": "LEAD_STRENGTH", ... },
    { "facet_name": "BASH", "facet_type": "hands_on_language", "content_tag": "LEAD_STRENGTH", ... },
    { "facet_name": "JavaScript", "facet_type": "hands_on_language", "content_tag": "LEAD_STRENGTH", ... },
    { "facet_name": "Node.js", "facet_type": "hands_on_framework", "content_tag": "SOLID_MATCH", ... }
  ]
}
```

**Processing:**

1. Adapter identifies LEAD_STRENGTH languages: PHP, BASH, JavaScript
2. Domain pattern matching: No single domain dominates → infer "fullstack"
3. Generate highlights tailored to fullstack pattern
4. Output: Template with featured_languages, domain_inference, 6 highlights

**Template Merge:**

```json
{
  "hiring_company": "Government of Canada",
  "hiring_position": "software developer",
  "featured_languages": "PHP, BASH, JavaScript",
  "domain_inference": "fullstack",
  "highlight_1": "<strong>End-to-end feature ownership</strong>; ...",
  ...
}
```

**Result:** Variable substitution in resume template produces targeted, domain-aware resume with relevant highlights.

## Testing

```bash
# Test adapter with existing correlation
python resume-machine/scripts/py_adapter_correlator_to_template.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json | jq .

# Test orchestration (dry-run)
python resume-machine/scripts/py_orchestrate_correlation_to_pdf.py \
  jobbankjobs/2026/04/05/correlation_software_developer_kanata.json \
  --dry-run
```

## Extending the Adapter

### Add New Domain

1. Add entry to `DOMAIN_PATTERNS` in `py_adapter_correlator_to_template.py`:

```python
DOMAIN_PATTERNS = {
    'your_domain': {
        'keywords': [...],
        'facet_types': [...],
        'highlights': [...]
    }
}
```

2. Add new template file: `resume-machine/role-based-templates/resume.your_domain.json`

3. Update `TEMPLATE_DOMAIN_MAP` for template selection (if using batch-process.sh integration).

### Custom Highlighting Logic

Modify `generate_template()` to use correlation scores instead of simple domain matching:

```python
# Example: weight highlights by correlation score
highlighted_facets = [
    c for c in correlations
    if c['content_tag'] == 'LEAD_STRENGTH' and c['score'] > 0.8
]
```

## Troubleshooting

| Issue                              | Solution                                                               |
| ---------------------------------- | ---------------------------------------------------------------------- |
| "Adapter output is not valid JSON" | Check correlation file path; validate with `jq .`                      |
| PDF not generated                  | Ensure `resumed` CLI is in PATH; check template variables substitution |
| Domain inference incorrect         | Review `DOMAIN_PATTERNS` keywords; extend matching logic               |

## Performance Notes

- Adapter processes correlation JSON in O(n) time (n = correlation count, typically 5–20)
- Negligible overhead; can run for every job without concern
- template injection is atomic (fail if jq merge fails)
