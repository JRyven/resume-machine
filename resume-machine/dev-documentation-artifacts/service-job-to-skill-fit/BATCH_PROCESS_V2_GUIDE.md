# batch-process-v2.sh — Adapter-Enhanced Resume Batch Processing

## Overview

`batch-process-v2.sh` extends the original batch processing workflow with intelligent template selection powered by the skill-job correlation adapter.

### Key Improvements

| Feature                  | v1 (original)               | v2 (new)                                 |
| ------------------------ | --------------------------- | ---------------------------------------- |
| **Template Selection**   | Manual (require user input) | Auto-detected by adapter                 |
| **Skill Analysis**       | ✗ None                      | ✓ Runs correlator on each job            |
| **Recommendations**      | ✗ None                      | ✓ Shows adapter suggestions              |
| **Fallback Logic**       | ✗ N/A                       | ✓ Manual override if adapter unavailable |
| **Non-interactive Mode** | ✗ No                        | ✓ `--auto-template` flag                 |
| **Dry-run Support**      | ✗ No                        | ✓ `--dry-run` flag                       |

## Usage

### Basic (Interactive)

```bash
./resume-machine/scripts/batch-process-v2.sh
```

- Extracts job postings from HTML
- Prompts once before starting
- For each job: runs correlator → adapter → shows recommendations
- User can accept adapter suggestion or override with custom template

### Auto-template (Non-interactive)

```bash
./resume-machine/scripts/batch-process-v2.sh --auto-template
```

- Skips all user prompts
- Automatically uses adapter recommendations
- Falls back to `default` template if adapter unavailable
- Useful for CI/CD or scheduled batch jobs

### Dry-run Preview

```bash
./resume-machine/scripts/batch-process-v2.sh --dry-run
```

- Shows what would happen without generating PDFs
- Useful for validation before full run

### Combined Flags

```bash
./resume-machine/scripts/batch-process-v2.sh --auto-template --dry-run
```

- Non-interactive + preview mode

### Environment Variables

```bash
# Override input directory (where HTML files are)
INPUT_DIR=/custom/path/to/jobbankjobs ./batch-process-v2.sh

# Skip HTML extraction (use existing resume-machine-queue.json)
SKIP_EXTRACT=true ./batch-process-v2.sh
```

## Workflow v2

```
┌─ Resume Machine Queue ────────────────────────┐
│ [Software Developer @ Company A]              │
│ [Data Engineer @ Company B]                   │
│ [Engineering Manager @ Company C]             │
└──────────┬──────────────────────────────────┘
           │
           ↓
      ┌────────────┐
      │ For each   │
      │ job entry  │
      └────┬───────┘
           │
           ↓
   ┌───────────────────┐
   │ role-template = ? │
   └────────┬──────────┘
            │
    ┌───────┴────────┐
    │                │
    v                v
 [Auto]         [Manual]
    │                │
    ↓                │
┌─────────────────┐  │
│ Find job JSON   │  │
└────────┬────────┘  │
         │           │
         ↓           │
┌─────────────────┐  │
│ Run correlator  │  │
└────────┬────────┘  │
         │           │
         ↓           │
┌─────────────────┐  │
│ Run adapter     │  │
└────────┬────────┘  │
         │           │
         ↓           │
 ┌─────────────────────────────────────────┐
 │ Display recommendation to user          │
 │    Domain: fullstack                    │
 │    Languages: PHP, BASH, JavaScript     │
 │    Highlights: [6 domain-specific]      │
 └──────────┬──────────────────────────────┘
            │
            ↓ (user accepts or overrides)
 ┌──────────────────────────────────────────┐
 │ Select template (inferred or manual)     │
 └──────────┬───────────────────────────────┘
            │
            ↓
 ┌──────────────────────────────────────────┐
 │ Merge template + company/position        │
 │ into resume.unique-data.json             │
 └──────────┬───────────────────────────────┘
            │
            ↓
 ┌──────────────────────────────────────────┐
 │ preprocess-resume.js                     │
 │ (variable substitution)                  │
 └──────────┬───────────────────────────────┘
            │
            ↓
 ┌──────────────────────────────────────────┐
 │ resumed export → resume.json             │
 │    (generates from template)             │
 └──────────┬───────────────────────────────┘
            │
            ↓
 ┌──────────────────────────────────────────┐
 │ Generate PDF                             │
 │    artifacts/resume-*.pdf                │
 └──────────────────────────────────────────┘
```

## Adapter Integration Details

### How Template Selection Works

#### 1. **Auto Mode** (`role-template: "auto"`)

```bash
# Queue entry with "auto"
{
  "title": "Software Developer",
  "company": "Acme Corp",
  "role-template": "auto"
}
```

**Process:**

- Find corresponding job JSON file in `jobbankjobs/`
- Run `py_skill_job_correlator.py` → generates `correlation_*.json`
- Run `py_adapter_correlator_to_template.py` → returns template recommendations
- Extract inferred domain (e.g., "fullstack", "backend", "devops")

**Result:**

```json
{
  "featured_languages": "PHP, BASH, JavaScript",
  "domain_inference": "fullstack",
  "highlight_1": "<strong>End-to-end feature ownership</strong>; ...",
  ...
}
```

#### 2. **Manual Mode** (explicit `role-template: "backend"`, etc.)

- Skip correlator/adapter
- Use specified template directly
- Useful for overriding auto-detection

### Fallback Logic

| Scenario                        | Behavior                                            |
| ------------------------------- | --------------------------------------------------- |
| Correlator runs successfully    | Use adapter-inferred template                       |
| Adapter suggests generic domain | Prompt user or use `default` (if `--auto-template`) |
| Job JSON not found              | Fall back to manual template selection              |
| All fails                       | Use `resume.defaults.json`                          |

### Conversation Example

```
╔═══════════════════════════════════════════════════════════════╗
║ Processing: Acme Corp — Software Developer
╚═══════════════════════════════════════════════════════════════╝
Template mode: auto (adapter-driven)
  Running correlator for job JSON...
  Running adapter for template inference...

  ╭─ Adapter Recommendation ─────────────────────────
  │ Job: Software Developer
  │ Domain:    fullstack
  │ Languages: PHP, BASH, JavaScript
  │ Highlights:
  │   • End-to-end feature ownership; database → API → UI
  │   • Modern JavaScript ecosystems; Node.js servers
  │   • Database design & optimization; schema modeling
  ╰────────────────────────────────────────────────────

✓ Using adapter-inferred template: fullstack

Sanitizing: company_doc="Acme Corp", title_doc="Software Developer"
✓ Generated: artifacts/resume-James-Valeii-Acme-Corp-Software-Developer.pdf
```

## Configuration

### Default Paths (from config.yaml)

```yaml
# resume-machine/config.yaml
input_dir: 'jobbankjobs/2026/04/05' # Override with INPUT_DIR env var
```

### Template Files

Templates live in `resume-machine/role-based-templates/`:

- `resume.defaults.json` – Default/fallback
- `resume.devops.json` – DevOps-focused
- `resume.manager.json` – Management-focused
- `resume.backend.json`, `resume.frontend.json`, etc.

### Adapter Domains

Recognized by adapter (from `DOMAIN_PATTERNS`):

- `fullstack` – Full-stack web development
- `backend` – Backend/server-side
- `frontend` – Frontend/client-side UI
- `devops` – Infrastructure & reliability
- `database` – Data-intensive systems
- `ml_ai` – Machine learning & data science
- `manager` – Team leadership

## Troubleshooting

### Issue: "Adapter output is not valid JSON"

**Solution:** Check correlation file exists and is well-formed

```bash
cat jobbankjobs/2026/04/05/correlation_*.json | jq .
```

### Issue: "Correlator unavailable; falling back to manual"

**Solution:** Ensure job JSON exists and is discoverable

```bash
find jobbankjobs -name "*.json" | head -5
```

### Issue: All PDFs use `default` template

**Solution:**

1. Check if correlator is running: add `set -x` to enable debug
2. Verify adapter pattern matches your job titles
3. Extend `DOMAIN_PATTERNS` in adapter for new skill domains

### Issue: "Template mode: manual" but didn't specify

**Solution:** Queue entry likely had `role-template` field set; either:

- Clear it to `null` (defaults to "auto")
- Edit `resume-machine/resume-machine-queue.json` directly

## Comparison: When to Use v1 vs v2

### Use v1 (batch-process.sh) when:

- You prefer explicit, manual template control
- You have few jobs to process
- You want the original simple workflow
- You're debugging template selection

### Use v2 (batch-process-v2.sh) when:

- You want automated, intelligent template selection
- You're processing many jobs
- You want skill-job matching insights
- You're running in CI/CD (with `--auto-template`)
- You want consistent domain-aware templates

## Performance Notes

- **Correlator:** ~2-5 seconds per job (depends on job description length)
- **Adapter:** <1 second per correlation
- **Batch processing:** ~200-300 PDF generations per minute (limited by `resumed` CLI)

For 50 jobs:

- **v1:** ~2-3 minutes (correlation skipped)
- **v2:** ~5-7 minutes (includes correlator + adapter)

Trade-off: +2-4 minutes upfront investment for intelligent, domain-aware templates.

## Examples

### Example 1: Process with auto-template, no prompts

```bash
cd /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv
INPUT_DIR=jobbankjobs/2026/04/05 ./resume-machine/scripts/batch-process-v2.sh --auto-template
```

### Example 2: Dry-run to preview recommendations

```bash
./resume-machine/scripts/batch-process-v2.sh --dry-run
# Review recommendations, then rerun without --dry-run
```

### Example 3: Manual override for specific job

```bash
# Edit queue.json
jq '.[] | select(.title | contains("Manager")) | .["role-template"] = "manager"' \
  resume-machine/resume-machine-queue.json

# Then run (will use "manager" template for that job, adapter for others)
./resume-machine/scripts/batch-process-v2.sh --auto-template
```

## Next Steps

1. **Test v2 with dry-run:** `./batch-process-v2.sh --dry-run`
2. **Compare recommendations** with your manual template choices
3. **Adjust `DOMAIN_PATTERNS`** if needed for your specific roles
4. **Integrate into CI/CD** using `--auto-template` flag

## See Also

- [ADAPTER_README.md](ADAPTER_README.md) – Adapter architecture
- [INTEGRATION_GUIDE.sh](INTEGRATION_GUIDE.sh) – Integration examples
- [py_adapter_correlator_to_template.py](py_adapter_correlator_to_template.py) – Adapter source
- [py_orchestrate_correlation_to_pdf.py](py_orchestrate_correlation_to_pdf.py) – Standalone orchestration
