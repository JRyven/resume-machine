# Job Skill Analyzer: Modular Pipeline Architecture

## Overview

`job_skill_analyzer.py` implements a **modular, three-tier skill resolution pipeline** for extracting job requirements from Job Bank Canada HTML files and matching them against your skills inventory (`skills-index.json`).

**Key Design Principle:** Every stage of the pipeline is independently accessible, allowing flexible composition for different use cases.

---

## Pipeline Architecture

### Stage 1: Load & Index (`load_skills_index()`)

**Responsibility:** Load skills inventory and build lookup dictionaries.

```python
index = load_skills_index()

# Returns:
# {
#   'facet_by_name': {normalized_name → facet_entry},
#   'facet_by_id': {facet_id → facet_entry},
#   'raw_index': raw JSON data
# }
```

**Use Case:** Initialize before any matching operations.

---

### Stage 2: HTML Extraction (`extract_skills_from_posting()`)

**Responsibility:** Parse Job Bank HTML → structured sections with skill strings.

```python
sections = extract_skills_from_posting('job_posting.html')

# Returns:
# {
#   'Overview > Languages': ['English'],
#   'Responsibilities > Tasks': ['Write code', 'Test software', ...],
#   'Experience & Specialization > Computer and technology knowledge': [
#       'Python', 'AWS', 'Docker', ...
#   ],
#   ...
# }
```

**Sections Extracted:**

- Overview: Languages, Education, Experience, Work setting
- Responsibilities: Various task categories
- Experience & Specialization: Technical knowledge, areas of expertise
- Additional Information: Work conditions, personal suitability
- Benefits: Health, financial, long-term, other

**Use Case:** Extract raw skills before matching, or for data exploration.

---

### Stage 3: Skill Resolution (`resolve_facet()`)

**Responsibility:** Map raw skill strings → facet entries using three-tier matching.

#### Resolution Strategy

**Tier 1: Exact Match**

```python
'JavaScript' → matches 'javascript' (normalized)
```

**Tier 2: Alias Table**

- 201 entries mapping job posting terminology → canonical facet names
- Examples:
  - `'spring boot'` → `'Spring / SpringBoot'`
  - `'k8s'` → `'Kubernetes'`
  - `'unix shell scripting'` → `'BASH'`

**Tier 3: Substring Match** (conservative, only if len > 2)

- Matches if raw skill contains facet name, or facet name contains raw skill

```python
facet = resolve_facet('spring', index)
# Tier 2 (via ALIASES): → 'Spring / SpringBoot'

facet = resolve_facet('kubernetes', index)
# Tier 2 (via ALIASES): → 'Kubernetes'

facet = resolve_facet('foobar', index)
# No match → returns None
```

**Use Case:** Test individual skill strings, debug matching logic.

---

### Stage 4: Match Report Generation (`match_posting_to_skills()`)

**Responsibility:** Process all extracted skills, produce structured match report.

```python
report = match_posting_to_skills(sections, index)

# Returns:
# {
#   'summary': {
#     'total_skills_extracted': 44,
#     'matched_to_facets': 3,
#     'unmatched': 41,
#     'match_rate_pct': 6.8
#   },
#   'matched': [
#     {
#       'raw_skill': 'JavaScript Object Notation (JSON)',
#       'source_section': 'Responsibilities > Tasks',
#       'facet_id': 'facet.javascript',
#       'facet_name': 'JavaScript',
#       'facet_type': 'hands_on_language',
#       'skill_group': 'programming_languages',
#       'proficiency': 'expert',
#       'confidence': 10,
#       'years': 12,
#       'last_used': '2026-Q1',
#       'duplicate': False
#     },
#     ...
#   ],
#   'unmatched': [
#     {
#       'raw_skill': 'Cloud',
#       'source_section': 'Experience & Specialization > Computer and technology knowledge'
#     },
#     ...
#   ]
# }
```

**Deduplication:** Tracks duplicate matches across sections (same facet matched multiple times). Flagged in output but not silently dropped—reveals posting emphasis.

**Use Case:** Detailed analysis, gap identification, custom reporting.

---

### Stage 5: Reporting (`print_report()`, `save_match_report()`)

**Responsibility:** Format and persist match reports.

```python
# Console output
print_report(report, sections)

# JSON persistence
output_file = save_match_report(html_path, sections, report)
```

**Console Output Sections:**

- Summary statistics (extracted, matched, unmatched, success rate)
- Detailed matched skills (with metadata)
- Unmatched skills (for alias table expansion)
- Full extracted sections (raw data)

**JSON Output:**

```json
{
  "metadata": {
    "source": "Job Bank Canada",
    "extracted_date": "2026-04-10T22:23:22Z",
    "source_html": "..."
  },
  "extracted_sections": { ... },
  "match_report": { ... }
}
```

---

## Orchestration & Usage Patterns

### Pattern 1: Full Pipeline (Extract → Match → Report)

```python
from job_skill_analyzer import analyze_job_posting

result = analyze_job_posting('job_posting.html', verbose=True)
# Returns: {'sections': {...}, 'report': {...}, 'output_file': '...'}
```

**Use Case:** One-off job analysis.

---

### Pattern 2: Modular Access (Individual Stages)

```python
from job_skill_analyzer import (
    load_skills_index,
    extract_skills_from_posting,
    resolve_facet,
    match_posting_to_skills,
)

# Stage 1
index = load_skills_index()

# Stage 2
sections = extract_skills_from_posting('job.html')

# Stage 3: Test individual resolution
facet = resolve_facet('Docker', index)

# Stage 4: Full matching
report = match_posting_to_skills(sections, index)

# Custom processing here...
```

**Use Case:** Custom pipelines, data exploration, ML feature extraction.

---

### Pattern 3: Batch Processing

```python
from job_skill_analyzer import batch_analyze_job_postings

results = batch_analyze_job_postings(job_dir='jobbankjobs/2026/04/05/')
# Analyzes all *.html files, generates JSON reports for each
```

**Use Case:** Process 11 job postings in one command.

---

### Pattern 4: Filtering & Analysis

```python
results = batch_analyze_job_postings(verbose=False)

# Filter to high-match jobs
high_match = [
    r for r in results
    if r['success'] and r['result']['report']['summary']['match_rate_pct'] > 10
]

for job in high_match:
    print(f"{job['file']}: {job['result']['report']['summary']['match_rate_pct']}%")
```

**Use Case:** Identify best-fit opportunities.

---

### Pattern 5: Gap Analysis (Missing Aliases)

```python
results = batch_analyze_job_postings(verbose=False)

# Collect all unmatched skills
unmatched_skills = {}
for r in results:
    if r['success']:
        for unmatched in r['result']['report']['unmatched']:
            skill = unmatched['raw_skill']
            unmatched_skills[skill] = unmatched_skills.get(skill, 0) + 1

# Most common unmatched = candidates for ALIASES table
for skill, count in sorted(unmatched_skills.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"{skill}: {count} postings")
```

**Use Case:** Expand ALIASES table over time.

---

## Alias Table Maintenance

The `ALIASES` dictionary is the main thing you'll maintain as you process more job postings.

**Structure:**

```python
ALIASES: Dict[str, str] = {
    # Raw job posting term → canonical facet name
    'spring boot': 'Spring / SpringBoot',
    'k8s': 'Kubernetes',
    'unix shell scripting': 'BASH',
    ...
}
```

**Workflow:**

1. Run analyzer, note unmatched skills
2. Identify high-frequency unmatched terms
3. Determine canonical facet name from `skills-index.json`
4. Add entry to `ALIASES`
5. Re-run analyzer to verify match

**Example Addition:**

```python
# From gap analysis: "Cloud" appears in 7 postings
# Check skills-index: no exact match for "cloud"
# Likely a strategic domain or platform capability
# Add temporary entry:
'cloud': 'AWS',  # Or could be 'Azure', 'Google Cloud Platform'
# Or create new facet if needed
```

---

## CLI Usage

### Single Job Analysis

```bash
python3 job_skill_analyzer.py 'path/to/job.html'
```

Outputs:

- Pretty-printed report to console
- JSON file with same name as HTML file

### Batch Analysis

```bash
python3 job_skill_analyzer.py
```

Analyzes all \*.html in `JOB_HTML_DIR` (default: `jobbankjobs/2026/04/05/`)

Outputs:

- One JSON file per HTML file
- Summary line showing total files processed

---

## Examples

See `USAGE_EXAMPLES.py` for 8 complete usage scenarios:

1. Inspect skills index
2. Extract from single posting
3. Test skill resolution
4. Full pipeline with verbose output
5. Custom report generation
6. Batch processing with filtering
7. Gap analysis for alias expansion
8. Full data access for downstream processing

---

## Integration with Other Tools

### Resume Profile Generation

```python
# Load resume + index
resume_facets = load_resume_skills()
job_report = analyze_job_posting('job.html')

# Compare
matched = set(resume_facets) & set(job_report['matched'])
gaps = set(job_report['matched']) - set(resume_facets)
```

### Cover Letter Generation

```python
# Use matched skills + source sections for targeting
for matched_skill in job_report['matched']:
    section = matched_skill['source_section']
    # Generate paragraph about this skill for cover letter
```

### Candidate Ranking

```python
# Score jobs by facet match, specificity, etc.
score = job_report['summary']['match_rate_pct']
weighted_skills = sum(s['years'] for s in job_report['matched'] if not s['duplicate'])
```

---

## Key Design Decisions

### Three-Tier Resolution

- **Benefit:** Progressive confidence levels, reducing false positives
- **Downside:** May miss some matches in tier 3 (substring fallback)
- **Tuning:** Adjust substring matching logic or tier order as needed

### Alias Table vs. Facet Expansion

- **Question:** When to add an alias vs. create a new facet?
- **Answer:** Alias if skill is a variant/synonym of existing facet (e.g., `k8s` → `Kubernetes`). Create facet if it's a genuinely new capability (e.g., new language)

### Deduplication Tracking

- **Design:** Flag duplicate matches rather than silently drop them
- **Rationale:** Reveals posting emphasis (high skill importance)
- **Use Case:** Weight repeated matches more heavily in scoring

### Section-Aware Extraction

- **Design:** Preserve source section for each skill
- **Benefit:** Can weight skills differently by section (e.g., specialization vs. responsibilities)

---

## Performance Notes

- **Index loading:** ~10ms (one-time)
- **HTML parsing:** ~50ms per file
- **Matching:** ~5ms per report
- **Batch 11 files:** ~1 second total

---

## Extensibility

### Adding New Resolution Tiers

```python
def resolve_facet(raw_skill: str, index: Dict) -> Optional[Dict]:
    # Tier 4: Fuzzy matching (Levenshtein distance)
    if not result:
        best_match = fuzzy_match_candidate(raw_skill, index['facet_by_name'])
        if best_match and best_match[1] > 0.85:  # confidence threshold
            return best_match[0]
```

### Custom Section Filtering

```python
def match_posting_to_skills_filtered(sections, index, section_filter=[]):
    """Only match skills from specified sections"""
    # Modify skill_rows generation to filter by section_label
```

### Adding New HTML Structures

The extractor is already robust to variations in Job Bank HTML. To handle new sources:

```python
def extract_skills_from_posting(html_path: str, parser='job_bank') -> Dict:
    if parser == 'linkedin':
        return extract_from_linkedin(html_path)
    elif parser == 'job_bank':
        return extract_from_job_bank(html_path)
```

---

## Limitations & Future Work

- **Limitation:** Only matches skills already in `facet_catalog` (plus aliases)
- **Workaround:** Expand ALIASES table based on gap analysis
- **Future:** Add fuzzy matching tier, external skill database lookup

- **Limitation:** Basic substring matching may produce false positives
- **Workaround:** Review unmatched list regularly, prune noisy patterns
- **Future:** Machine learning-based entity linking

- **Limitation:** No semantic understanding of skill relationships
- **Workaround:** Manual curation of facet_catalog and ALIASES
- **Future:** Knowledge graph integration, skill clustering

---

## Questions?

For usage questions or pipeline modifications, check:

- `USAGE_EXAMPLES.py` — 8 complete working examples
- `skills-schema.json` — Facet types, proficiency levels, valid enums
- `skills-index.json` → `facet_catalog` — Your current inventory
