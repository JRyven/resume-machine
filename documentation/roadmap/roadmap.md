---
project_name: [PROJECT_NAME]
title: Unified Development Roadmap
description: Comprehensive roadmap for all project development phases from inception through production launch and ongoing maintenance.
last_updated: [YYYY-MM-DD]
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

### In Progress

⚠️ LIMIT: Only 1 project allowed in this section

#### Repair Linting

You hit a pre-commit hook (husky + lint-staged). lint-staged tried to run ESLint/Prettier on staged files, failed because ESLint has no config, so the hook aborted and Git reverted the staged changes.

Options to fix (pick one):

Add a minimal ESLint config (recommended quick fix):

```
cat > .eslintrc.json <<'JSON'
{
  "env": { "es2021": true, "node": true, "browser": true },
  "extends": ["eslint:recommended"],
  "parserOptions": { "ecmaVersion": 2021, "sourceType": "module" },
  "rules": {}
}
JSON

git add .eslintrc.json
git add -A
git commit -m "v0.0.4 Pivot to monorepo"
```

Run the ESLint initializer (guided)

```
npm init @eslint/config
# follow prompts, then:
git add -A
git commit -m "v0.0.4 Pivot to monorepo"
```

Diagnose lint-staged problems before committing:

```
npx lint-staged --debug
# or run prettier/eslint manually to see errors:
npx prettier --check .
npx eslint --ext .js,.ts src/ || npx eslint --ext .js,.ts --fix src/
```

### Backlog

#### [Upate role specific content variance to Abstract Areas of Expertise]

#### [Keyword Analysis]

https://github.com/srbhr/Resume-Matcher

#### [Batch Processing System for Resumes]

Building a batch processing system to ingest HTML job postings, preprocess resume data, and generate tailored cover letter/resume PDFs. Currently setting up HTML data extraction using Puppeteer and configuring the workflow with Bash scripts.

#### [HTML Data Extraction]

Extract key data from each HTML job posting file and save it into preprocess-batch-export-resume.json.

[Install Puppeteer]: Set up Node.js environment and install Puppeteer.

#### Project: MCP Server Setup & Verification

**Dependencies**: (Environment Setup)

Clone and configure the JSON Resume MCP server for AI-assisted editing.

**Tasks**:

- [ ] Clone `jsonresume/mcp` repository
- [ ] Install MCP dependencies: `npm install`
- [ ] Verify MCP server builds successfully
- [ ] Test MCP server with sample resume.json
- [ ] Document MCP endpoints and capabilities
- [ ] Configure MCP server for local development

```bash
cd jsonresume-mcp
npm install
npm run build
npm test  # Verify all tests pass
```

#### Project: MCP Integration & Testing

**Dependencies**: (MCP Setup), T7 (PDF Generation)

Integrate MCP server with resume workflow for AI-assisted editing.

**Tasks**:

- [ ] Configure MCP server to read from `content/` directory
- [ ] Test CRUD operations on resume sections
- [ ] Verify AI assistant can modify structured fields
- [ ] Test end-to-end: AI edit → composition → PDF generation
- [ ] Document MCP usage patterns
- [ ] Create example AI prompts for common edits
- [ ] Write integration tests

**Example AI Workflows**:

- "Add a new bullet point to my Goop experience emphasizing leadership"
- "Update my skills to include more DevOps tools"
- "Create a variant resume focusing on e-commerce experience"

### Complete

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
- PDF output: `artifacts/baseline-valeii-professional.pdf`
- Command: `resumed export artifacts/resume.json -t valeii-professional -o artifacts/baseline-valeii-professional.pdf`

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
- Full resume PDF: `artifacts/full-resume-valeii-professional.pdf` (2 pages, 341KB)
- Baseline PDF: `artifacts/baseline-valeii-professional.pdf` (1 page, 2.8KB)
- Documentation: Updated README with installation, usage, schema support, and specialized font requirements
- CI Integration: Theme builds successfully in monorepo pipeline
- Font Integration: Local specialized Noto fonts loaded via @font-face for offline compatibility:
  - Headers use Noto Serif Hentaigana Medium
  - Body text uses Noto Sans Cypro Minoan Regular
  - Meta elements use Noto Serif Display Italic

#### Project: Content Model Design

**Dependencies**: (MCP Setup)

Design YAML content architecture supporting base + role-specific composition.

**Tasks**:

- [x] Create `content/base.yaml` with static fields (name, contact, education)
- [x] Create `content/fragments/` directory structure
- [x] Design fragment schema for: experience, skills, projects
- [x] Document composition strategy in `docs/content-model.md`
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

Implement Python script to merge YAML fragments into valid JSON Resume.

**Tasks**:

- [x] Create `scripts/compose_resume.py`
- [x] Implement YAML loading with validation
- [x] Handle merge conflicts gracefully
- [x] Write comprehensive tests (pytest)

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

**Dependencies**: (PDF Generation CLI)

Automate validation and PDF generation on content changes.

**Tasks**:

- [x] Create GitHub Actions workflow (or equivalent)
- [ ] Run schema validation on YAML changes
- [ ] Build all role-specific PDFs
- [x] Store PDFs as build artifacts
- [ ] Compare against baseline (visual regression)
- [ ] Fail pipeline on validation errors
- [ ] Document CI setup in `docs/ci-cd.md`

**Triggers**:

- Push to `main` branch
- Pull requests modifying `content/`
- Manual workflow dispatch

**Status**: CI workflow added at `.github/workflows/ci.yml` to run tests and perform a dry-run build; artifacts uploaded when present (2025-12-17).

---
