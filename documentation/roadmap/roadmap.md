---
project_name: JSON CV
title: Unified Development Roadmap
description: Comprehensive roadmap for all project development phases from inception through production launch and ongoing maintenance.
last_updated: 2025-12-19
cleardoc_version: 2.3.0
keywords: [roadmap, development, planning, maintenance, growth]
---

# Unified Development Roadmap

This roadmap covers all project development phases from inception through production launch and ongoing maintenance. It provides a unified approach to tracking work across the entire project lifecycle, whether you're in the initial development phase, managing post-launch stabilization, or planning long-term enhancements.

For guidance on using and updating this roadmap, see [How to Use This Roadmap](#how-to-use-this-roadmap) below. This repository has defined risk management considerations; please review [Risk Management](#risk-management) in this document.

---

## How to Use This Roadmap

### Adding New Projects

1. Identify the project scope and define clear deliverables
2. Create an H4 heading with the project name in the appropriate lifecycle section (typically Backlog)
3. Include a status section with current context and any relevant code examples
4. Add metadata fields: `created`, `dependencies`, `priority`
5. Structure tasks within the project using H5 headings organized by their lifecycle (In Progress, Backlog, Complete)

### Updating Project Status

Projects follow this linear progression:

```
Backlog → In Progress → Complete
                    ↘
                    Rejected (if abandoned)
```

**WIP Limits Enforcement:**

- Only 1 project may be in "In Progress" at a time
- Enforce this limit manually by reviewing this document regularly
- Move completed projects to "Complete" before starting new ones

---

## Risk Management

### Common Risks in Development Workflows

**1. Context Loss Between Work Sessions**

- Risk: Team members lose track of project state across work sessions
- Mitigation: Maintain detailed status sections in each project

**2. Scope Creep**

- Risk: Projects expand beyond original scope without tracking
- Mitigation: Use dependency fields to identify blockers; update metadata when scope changes

**3. WIP Limit Violations**

- Risk: Multiple projects in progress lead to context switching and slower delivery
- Mitigation: Enforce 1 project in progress limit; review this document weekly

**4. Stale Documentation**

- Risk: Roadmap diverges from actual project state
- Mitigation: Update roadmap during project sync meetings

---

## Development Goals

All projects required to achieve milestones (MVP launch, feature releases, maintenance goals) are tracked in this section using the Development Goals tracking system. For complete documentation of the tracking structure, metadata requirements, and modification rules, see the [Roadmap Specification](./specification.md).

For guidance on updating this roadmap, see [How to Use This Roadmap](#how-to-use-this-roadmap) below.

---

### 🔄 In Progress

**Dependencies**: (Theme Freeze), T6 (Composition Engine)

Create unified CLI wrapper for the complete resume generation pipeline.

**Tasks**:

- [x] Create [scripts/build_resume.py](scripts/build_resume.py)
- [x] Integrate composition engine
- [ ] Call `resumed` with frozen theme
- [ ] Implement filename pattern: `{firstname}-{lastname}-{role}-{YYYYMMDD}.pdf`
- [x] Add metadata injection (generation date, role key)
- [x] Implement dry-run mode
- [ ] Add verbose logging
- [x] Write integration tests

**CLI Interface**:

```bash
python build_resume.py \
  --role senior-engineer \
  --output artifacts/ \
  --validate \
  --verbose
```

**Output**: `james-valeii-senior-engineer-20251217.pdf`

**Status**: `scripts/build_resume.py` implemented with dry-run and metadata sidecar; integration tests for dry-run pass. `resumed` invocation is mocked in tests (2025-12-17).

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

### 📋 Backlog

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

---

### ✅ Complete

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

Fork selected theme, apply custom EB Garamond styling, and freeze for production use.

**Tasks**:

- [x] Fork theme into `packages/themes/jsonresume-theme-valeii-professional/`
- [x] Verify no layout breaks with edge cases
- [x] Generate comparison PDF against baseline
- [x] Prepare theme package for distribution
- [x] Document theme inclusion in README and CI

**Testing Checklist**:

- Single-line vs multi-line bullets ✓
- 1-year vs 10-year work history ✓
- 3 skills vs 30 skills ✓
- Various text lengths in summaries ✓

**Status**: Completed (custom theme created with EB Garamond, tested, packaged, and documented) — 2025-12-19

**Validation**:

- Theme package: `packages/themes/jsonresume-theme-valeii-professional/`
- Full resume PDF: `artifacts/full-resume-valeii-professional.pdf` (2 pages, 341KB)
- Baseline PDF: `artifacts/baseline-valeii-professional.pdf` (1 page, 2.8KB)
- Documentation: Updated README with installation, usage, and schema support
- CI Integration: Theme builds successfully in monorepo pipeline

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

#### 🚫 Rejected

[No rejected tasks yet.]

## Risk Register

| Risk                                      | Impact | Mitigation                                                        |
| ----------------------------------------- | ------ | ----------------------------------------------------------------- |
| Theme produces inconsistent PDFs          | High   | Freeze theme, test with content variations, use visual regression |
| MCP server incompatible with workflow     | Medium | Test early (T2), maintain fallback manual editing process         |
| JSON Resume schema changes                | Low    | Pin schema version, automate validation                           |
| Font rendering varies across environments | Medium | Vendor fonts locally, test on multiple OS                         |
| AI suggestions violate schema             | Medium | Validate all changes before composition                           |

---

## Quick Start (Once Complete)

```bash
# 1. Compose resume for specific role
python scripts/compose_resume.py --role senior-engineer

# 2. Generate PDF
python scripts/build_resume.py --role senior-engineer

# 3. AI-assisted editing (via MCP)
# Use Claude or other AI assistant with MCP integration
# Example: "Add DevOps achievement to Goop experience"

# 4. Rebuild after changes
python scripts/build_resume.py --role senior-engineer --validate
```
