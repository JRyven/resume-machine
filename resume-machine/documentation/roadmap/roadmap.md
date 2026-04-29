---
project_name: Resume Machine
title: Unified Development Roadmap
description: Comprehensive roadmap for all project development phases from inception through production launch and ongoing maintenance.
last_updated: [2026-04-29]
cleardoc_version: 2.3.0
keywords: [roadmap, development, planning, maintenance, growth]
---

# Unified Development Roadmap

All projects required to achieve the Unified Email Routing Schema implementation are tracked in this section using the Development Goals tracking system. For complete documentation of the tracking structure, metadata requirements, and modification rules, see the [Roadmap Specification](./specification.md).

## Special Implementation Notes

### Config

Configuration settings for production (live) and develop (unit test) need to be identical.

`config/app.yaml` should set all COMMON configurations for production and development.
To maintain DRY, SOLID, and code with low cognative burden, app.yaml may offload boilerplate to additional configuration files in `config/`

`config/develop/develop.yaml` and `config/production/production.yaml` should hold `.yaml` configuration rules that are distinct for the enviornments

When `config/app.yaml` is set to use `develop`, `yaml` files from `/config/develop` must be used to implement unit test application functionality.

When `config/app.yaml` is set to use `production`, `yaml` files from `/config/production` must be used to implement live application functionality.

Ensure that we're developing a robust representation of test data in `/mock-data` to use for `develop` unit tests.

---

## Projects

### In Progress

⚠️ LIMIT: Only 1 project allowed in this section

#### [Optimizations]
'''
Establishing better organization system within /scripts/ that makes the role of each file clearer, adding a shared naming helper used by batch-process.sh so both runners behave identically, updating py_skill_job_correlator.py to populate metadata.job_title and metadata.employer upstream, and refactoring DOMAIN_PATTERNS to use template files.
'''
created: 2025-12-29
dependencies: [none]
priority: high

##### [Establish better organization system within /scripts/ that makes the role of each file clearer]
Reorganizing the scripts directory to improve clarity and maintainability. The scripts will be grouped by functionality:

- `data_processing/` - Scripts for data extraction and preprocessing
- `template_management/` - Scripts for template handling and generation
- `orchestration/` - Scripts that coordinate the overall workflow
- `utilities/` - Helper scripts and utilities used across the system

Each script will have a clear purpose and be documented with usage examples.

- [ ] [Create new script directory structure]: Implement the new directory organization with data_processing/, template_management/, orchestration/, and utilities/ folders.
- [ ] [Update existing scripts]: Move existing scripts to their appropriate new locations and update any references.
- [ ] [Document script purposes]: Add README files to each directory explaining the purpose and usage of scripts within.
- [ ] [Test directory structure]: Verify that all scripts run correctly with the new organization.

##### [Add a shared naming helper used by batch-process.sh so both runners behave identically]
Create a `naming_utils.py` file in the scripts directory with functions for filename sanitization.

- [ ] [Create naming_utils.py]: Implement the Python utility with functions for filename sanitization:
  - `sanitize_for_filename(s: str) -> str`: Clean strings for use in filenames (remove special characters, normalize spaces, etc.)
  - `derive_basename_from_job_json(job_json_path: Optional[str]) -> str`: Extract clean basename from job JSON paths
  - `build_dated_artifact_path(artifacts_dir: Path, base_name: str) -> Path`: Create dated directory structure for artifacts
- [ ] [Update batch-process.sh]: Modify the shell script to use the Python utility instead of JavaScript.
- [ ] [Update py_orchestrate_correlation_to_pdf.py]: Update the Python script to import and use the same utility.
- [ ] [Test consistency]: Ensure both scripts produce identical filename formatting for consistency.

##### [Update py_skill_job_correlator.py to populate metadata.job_title and metadata.employer upstream]
Modify `py_skill_job_correlator.py` to extract and populate `metadata.job_title` and `metadata.employer` fields.

- [ ] [Extract job title and employer]: Modify the correlator to extract job title and employer from job posting data.
- [ ] [Populate metadata fields]: Update the correlation process to ensure these fields are properly set before processing.
- [ ] [Update filename generation]: Modify filename generation logic to use the new metadata fields.
- [ ] [Test metadata population]: Verify that the metadata fields are correctly populated and used in the workflow.

##### [Refactor DOMAIN_PATTERNS to Use Template Files]
The current implementation has domain patterns hardcoded within the Python script, while template files in the role-based-templates directory contain similar content but are separate. This creates duplication but provides performance and portability benefits. This task involves implementing a hybrid approach that reduces duplication while maintaining script functionality.

- [ ] [Analyze current DOMAIN_PATTERNS implementation in Python script]: Review the existing implementation to understand how patterns are currently used.
- [ ] [Review template files in role-based-templates directory]: Examine the template files to understand their structure and content.
- [ ] [Design hybrid approach that reads from template files while maintaining core logic in code]: Create a design that combines both approaches.
- [ ] [Implement solution to reduce duplication between script and template files]: Implement the hybrid approach.
- [ ] [Test that the refactored approach maintains performance and portability]: Verify that the refactored approach works correctly.
- [ ] [Update documentation to reflect the new hybrid approach]: Update any relevant documentation.

### Backlog

#### [Migrate to a system modifyable system]

Output correlated resume data as json
- json with resume file name (EG: resume-James-software-developer-Kanata-ON-Job-posting-Job-Bank.json)

Include cover letter data in correlated resume data
- codify correlation-built cover letters

Duplicate manual-cover-letter.html as resume-machine.html.
- extend resume-machine.html to run on a local python server
- permit correlated resume data to be selected and rendered directly
  - include select filed to filter by month path
  - include select filed to filter by day path
  - include a searchable select field to filter by specific correlated resume json file
  - selected correlated resume json file hydrates the page
- user clicks print to generate PDF through browser UX

#### [Keyword Analysis]

https://github.com/srbhr/Resume-Matcher

#### Project: MCP Server Setup & Verification
'''
Clone and configure the JSON Resume MCP server for AI-assisted editing.
'''
created: 2025-12-29
dependencies: [Environment Setup]
priority: high

**Tasks**:

- [ ] [Clone `jsonresume/mcp` repository]: Clone the repository to the local development environment.
- [ ] [Install MCP dependencies]: Run `npm install` to install all required dependencies.
- [ ] [Verify MCP server builds successfully]: Run build commands to ensure the server compiles without errors.
- [ ] [Test MCP server with sample resume.json]: Validate that the server works with a sample resume file.
- [ ] [Document MCP endpoints and capabilities]: Create documentation for all available endpoints and their functionality.
- [ ] [Configure MCP server for local development]: Set up the server for local development and testing.

```bash
cd jsonresume-mcp
npm install
npm run build
npm test  # Verify all tests pass
```

#### Project: MCP Integration & Testing
'''
Integrate MCP server with resume workflow for AI-assisted editing.
'''
created: 2025-12-29
dependencies: [MCP Setup, PDF Generation]
priority: high

**Tasks**:

- [ ] [Configure MCP server to read from `content/` directory]: Set up the MCP server to properly read and process content from the content directory.
- [ ] [Test CRUD operations on resume sections]: Validate that Create, Read, Update, and Delete operations work correctly on resume sections.
- [ ] [Verify AI assistant can modify structured fields]: Ensure the AI assistant can properly modify structured fields in the resume.
- [ ] [Test end-to-end: AI edit → composition → PDF generation]: Run a complete workflow test from AI editing through to PDF generation.
- [ ] [Document MCP usage patterns]: Create documentation for common usage patterns and workflows.
- [ ] [Create example AI prompts for common edits]: Develop example prompts for common editing tasks.
- [ ] [Write integration tests]: Implement tests to verify the integration works correctly.

**Example AI Workflows**:

- "Add a new bullet point to my Goop experience emphasizing leadership"
- "Update my skills to include more DevOps tools"
- "Create a variant resume focusing on e-commerce experience"

### Complete

#### [Batch Processing System for Resumes]

Building a batch processing system to ingest HTML job postings, preprocess resume data, and generate tailored cover letter/resume PDFs. Currently setting up HTML data extraction using Puppeteer and configuring the workflow with Bash scripts.

#### [HTML Data Extraction]

Extract key data from each HTML job posting file and save it into preprocess-batch-export-resume.json.

[Install Puppeteer]: Set up Node.js environment and install Puppeteer.

#### [Batch Processing System for Resumes]

#### Project: Environment Setup & Dependencies

**Dependencies**: None

Install and verify all required tooling for the resume automation pipeline.

**Tasks**:

- [x] Node.js ≥18 installed and verified (`node --version`)
- [x] Package manager available (npm or pnpm)
- [x] Python 3.10+ installed with pip
- [x] Virtual environment created: `python -m venv .venv`
- [x] Git configured for version control
- [x] `resumed` installed globally: `npm install -g resumed`
- [x] Verify resumed works: `resumed --version`

**Status**: Completed (resumed installed, Python venv created, requirements validated) — 2025-12-18

**Validation**:

```bash
node --version  # Should show v18+
python --version  # Should show 3.10+
resumed --version  # Should show current version
```

#### [Environment Setup & Dependencies]

#### Project: Theme Selection & Baseline

**Dependencies**: (Environment Setup)

Select and validate a resume theme for consistent PDF generation.

**Tasks**:

- [x] Test 1 themes with your resume.json
- [x] Select final theme based on: typography, spacing, ATS compatibility

**Decision Factors**:

- Typography quality (EB Garamond support preferred)
- Clean, professional layout
- ATS-friendly structure
- Minimal visual noise

**Status**: Completed (custom valeii-professional theme created, PDF generated) — 2025-12-18

**Validation**:

- Theme package: `packages/themes/jsonresume-theme-valeii-professional/`
- PDF output: `resume-machine/artifacts/baseline-valeii-professional.pdf`
- Command: `resumed export resume-machine/artifacts/resume.json -t valeii-professional -o resume-machine/artifacts/baseline-valeii-professional.pdf`

#### Project: Theme Customization & Freeze

**Dependencies**: (Theme Selection)

Fork selected theme, apply custom specialized Noto font styling, and freeze for production use.

**Tasks**:

- [x] Fork theme into `packages/themes/jsonresume-theme-valeii-professional/`
- [x] Verify no layout breaks with edge cases
- [x] Generate comparison PDF against baseline
- [x] Prepare theme package for distribution
- [x] Document theme inclusion in README and CI
- [x] Integrate local specialized Noto fonts for offline rendering:
  - Headers: Noto Serif Hentaigana Medium
  - Body: Noto Sans Cypro Minoan Regular
  - Meta: Noto Serif Display Italic

**Testing Checklist**:

- Single-line vs multi-line bullets ✓
- 1-year vs 10-year work history ✓
- 3 skills vs 30 skills ✓
- Various text lengths in summaries ✓

**Status**: Completed (custom theme created with specialized Noto fonts, tested, packaged, and documented) — 2025-12-19

**Validation**:

- Theme package: `packages/themes/jsonresume-theme-valeii-professional/`
- Full resume PDF: `resume-machine/artifacts/full-resume-valeii-professional.pdf` (2 pages, 341KB)
- Baseline PDF: `resume-machine/artifacts/baseline-valeii-professional.pdf` (1 page, 2.8KB)
- Documentation: Updated README with installation, usage, schema support, and specialized font requirements
- CI Integration: Theme builds successfully in monorepo pipeline
- Font Integration: Local specialized Noto fonts loaded via @font-face for offline compatibility:
  - Headers use Noto Serif Hentaigana Medium
  - Body text uses Noto Sans Cypro Minoan Regular
  - Meta elements use Noto Serif Display Italic

#### Project: Content Model Design
'''
Design YAML content architecture supporting base + role-specific composition.
'''
created: 2025-12-29
dependencies: [MCP Setup]
priority: high

**Tasks**:

- [x] [Create `content/base.yaml` with static fields]: Create the base YAML file with static fields (name, contact, education).
- [x] [Create `content/fragments/` directory structure]: Set up the directory structure for content fragments.
- [x] [Design fragment schema for: experience, skills, projects]: Define the schema for different types of content fragments.
- [x] [Document composition strategy in `docs/content-model.md`]: Create documentation for the composition strategy.
      **File Structure**:

```
│   ├── experience/
│   │   ├── goop.yaml
│   │   ├── no-borders.yaml
│   │   └── boiling-pot.yaml
│   ├── skills/
│   │   ├── full-stack.yaml
│   │   ├── leadership.yaml
│       ├── tech-lead.yaml
│       └── founder.yaml
```

**Tasks**:

- [x] [Create `scripts/compose_resume.py`]: Implement the Python script to merge YAML fragments into valid JSON Resume.
- [x] [Implement YAML loading with validation]: Add validation to the YAML loading process.
- [x] [Handle merge conflicts gracefully]: Implement conflict resolution for merge operations.
- [x] [Write comprehensive tests (pytest)]: Create tests to verify the composition functionality.

**Validation**:

```bash
python compose_resume.py \
  --base content/base.yaml \
  --output build/resume.json \
  --validate
```

**Status**: Implementation scaffolded — `scripts/compose_resume.py` created; unit tests for merge logic pass (2025-12-17).

- T6: Composition Engine — completed 2025-12-17

---

### Rejected

#### Project: CI/CD Pipeline
'''
Automate validation and PDF generation on content changes.
'''
created: 2025-12-29
dependencies: [PDF Generation CLI]
priority: medium

**Tasks**:

- [x] [Create GitHub Actions workflow (or equivalent)]: Set up the CI/CD workflow using GitHub Actions.
- [ ] [Run schema validation on YAML changes]: Implement schema validation for YAML content changes.
- [ ] [Build all role-specific PDFs]: Configure the pipeline to build PDFs for all role-specific variants.
- [x] [Store PDFs as build artifacts]: Configure artifact storage for generated PDFs.
- [ ] [Compare against baseline (visual regression)]: Implement visual regression testing against baseline.
- [ ] [Fail pipeline on validation errors]: Configure the pipeline to fail on validation errors.
- [ ] [Document CI setup in `docs/ci-cd.md`]: Create documentation for the CI/CD setup.

**Triggers**:

- Push to `main` branch
- Pull requests modifying `content/`
- Manual workflow dispatch

**Status**: CI workflow added at `.github/workflows/ci.yml` to run tests and perform a dry-run build; artifacts uploaded when present (2025-12-17).

---
