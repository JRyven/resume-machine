# Batch Process v2 - Quick Start

## What's New

**batch-process-v2.sh** now integrates the adapter to automatically select resume templates based on skill-job correlation analysis.

### Before (v1)

```bash
$ ./batch-process.sh
# Manual: Select "backend", "frontend", "devops", etc. for each job
```

### After (v2)

```bash
$ ./batch-process-v2.sh --auto-template
# Automatic: Analyzes job requirements → infers best template
# Example output shows: "Domain: fullstack, Languages: PHP, BASH, JavaScript"
```

## Key Differences

| Aspect             | v1             | v2                                          |
| ------------------ | -------------- | ------------------------------------------- |
| Template selection | Manual per job | Auto-detected by adapter                    |
| Skill analysis     | None           | Correlates skills with job                  |
| Recommendations    | None           | Shows domain + featured languages           |
| User prompts       | Many           | 1 (initial review) if not `--auto-template` |
| Non-interactive    | ✗              | ✓ `--auto-template` flag                    |
| Dry-run support    | ✗              | ✓ `--dry-run` flag                          |

## 3-Minute Setup

### 1. Test Dry-Run

```bash
cd /Users/jamesvaleil/Desktop/db/0-projects/active/0-career-cv
./resume-machine/scripts/batch-process-v2.sh --dry-run
```

Shows what would happen without generating PDFs.

### 2. Run with User Approval

```bash
./resume-machine/scripts/batch-process-v2.sh
```

Prompts once at start, then shows recommendations for each job. Accept or override.

### 3. Run Fully Automated

```bash
./resume-machine/scripts/batch-process-v2.sh --auto-template
```

Skips all prompts, uses adapter recommendations automatically.

## What Happens Under the Hood

For each job:

```
Queue entry with role-template: "auto"
    ↓
Find job JSON in jobbankjobs/
    ↓
Run py_skill_job_correlator.py (correlates skills)
    ↓
Run py_adapter_correlator_to_template.py (infers domain)
    ↓
Display recommendation:
  Domain: fullstack
  Languages: PHP, BASH, JavaScript
  Highlights: [6 domain-specific bullet points]
    ↓
User accepts → template = inferred domain
   OR
User overrides → template = custom choice
    ↓
Generate resume.json (with company/position + template highlights)
    ↓
Export PDF
```

## Output Example

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
✓ Generated: artifacts/resume-James-Valeii-Acme-Corp-Software-Developer.pdf
```

## When to Use Each Version

### Use v1 (batch-process.sh)

- You prefer full manual control
- You're testing/debugging templates
- You have a small batch

### Use v2 (batch-process-v2.sh)

- You want intelligent automation
- You're processing many jobs
- You want consistent, domain-aware resumes
- You're running in CI/CD

## Running in CI/CD

```bash
# GitHub Actions / GitLab CI example
- name: Generate resumes with adapter
  run: |
    cd /path/to/0-career-cv
    INPUT_DIR=jobbankjobs/2026/04/05 \
      ./resume-machine/scripts/batch-process-v2.sh --auto-template --skip-extract
```

## Files Added/Modified

| File                                   | Type          | Purpose                              |
| -------------------------------------- | ------------- | ------------------------------------ |
| `batch-process-v2.sh`                  | Script        | Main v2 orchestration                |
| `batch-process.sh`                     | Script        | Original (unchanged)                 |
| `py_adapter_correlator_to_template.py` | Handler       | Infers template from correlation     |
| `py_orchestrate_correlation_to_pdf.py` | Orchestrator  | Standalone end-to-end flow           |
| `ADAPTER_README.md`                    | Documentation | Adapter architecture + domains       |
| `INTEGRATION_GUIDE.sh`                 | Examples      | Code snippets for custom integration |
| `BATCH_PROCESS_V2_GUIDE.md`            | Reference     | Complete v2 documentation            |

## Troubleshooting

### "Adapter output is not valid JSON"

```bash
# Check correlation file
cat jobbankjobs/2026/04/05/correlation_*.json | jq .
```

### "Correlator unavailable; falling back to manual"

```bash
# Verify job JSON exists
find jobbankjobs -name "*.json" | head
```

### Using custom domain

```bash
# Extend DOMAIN_PATTERNS in py_adapter_correlator_to_template.py
# Then reference via role-template in queue
```

## Next Steps

1. ✅ Test: `./batch-process-v2.sh --dry-run`
2. ✅ Review recommendations
3. ✅ Run: `./batch-process-v2.sh --auto-template`
4. ✅ Compare with v1 results
5. ✅ Switch workflows if satisfied

## Full Docs

- [BATCH_PROCESS_V2_GUIDE.md](BATCH_PROCESS_V2_GUIDE.md) — Complete reference
- [ADAPTER_README.md](ADAPTER_README.md) — How adapter works
- [INTEGRATION_GUIDE.sh](INTEGRATION_GUIDE.sh) — Custom integration examples
