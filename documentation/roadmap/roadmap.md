---
project_name: JSON CV
title: Unified Development Roadmap
description: Comprehensive roadmap for all project development phases from inception through production launch and ongoing maintenance.
last_updated: 2025-12-17
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

### Tasks

#### 🔄 In Progress
⚠️ **LIMIT**: Maximum 2 tasks in this section

[No tasks currently in progress.]

---

#### 📋 Backlog

##### T1: Environment Setup & Dependencies
**Dependencies**: None

Install and verify all required tooling for the resume automation pipeline.

**Acceptance Criteria**:
- [ ] Node.js ≥18 installed and verified (`node --version`)
- [ ] Package manager available (npm or pnpm)
- [ ] Python 3.10+ installed with pip
- [ ] Virtual environment created: `python -m venv .venv`
- [ ] Git configured for version control
- [ ] `resumed` installed globally: `npm install -g resumed`
- [ ] Verify resumed works: `resumed --version`

**Validation**:
```bash
node --version  # Should show v18+
python --version  # Should show 3.10+
resumed --version  # Should show current version
```

---

##### T2: MCP Server Setup & Verification
**Dependencies**: T1 (Environment Setup)

Clone and configure the JSON Resume MCP server for AI-assisted editing.

**Acceptance Criteria**:
- [ ] Clone `jsonresume/mcp` repository
- [ ] Install MCP dependencies: `npm install`
- [ ] Verify MCP server builds successfully
- [ ] Test MCP server with sample resume.json
- [ ] Document MCP endpoints and capabilities
- [ ] Configure MCP server for local development

**Validation**:
```bash
cd jsonresume-mcp
npm install
npm run build
npm test  # Verify all tests pass
```

---

##### T3: Theme Selection & Baseline
**Dependencies**: T1 (Environment Setup)

Select and validate a resume theme for consistent PDF generation.

**Acceptance Criteria**:
- [ ] List available `resumed` themes: `resumed themes`
- [ ] Test 3-5 themes with your resume.json
- [ ] Select final theme based on: typography, spacing, ATS compatibility
- [ ] Generate baseline PDF from current resume
- [ ] Store baseline as `artifacts/baseline-resume.pdf`
- [ ] Document theme choice rationale in `docs/theme-selection.md`

**Decision Factors**:
- Typography quality (EB Garamond support preferred)
- Clean, professional layout
- ATS-friendly structure
- Minimal visual noise

---

##### T4: Theme Customization & Freeze
**Dependencies**: T3 (Theme Selection)

Fork selected theme, apply custom EB Garamond styling, and freeze for production use.

**Acceptance Criteria**:
- [ ] Fork theme into `themes/valeii-professional/`
- [ ] Replace fonts with EB Garamond (Google Fonts or local)
- [ ] Adjust typography scale to match current resume
- [ ] Test with sample content variations (short/long bullets)
- [ ] Verify no layout breaks with edge cases
- [ ] Generate comparison PDF against baseline
- [ ] Commit frozen theme with documentation
- [ ] Tag theme version: `v1.0.0`

**Testing Checklist**:
- Single-line vs multi-line bullets
- 1-year vs 10-year work history
- 3 skills vs 30 skills
- Various text lengths in summaries

---

#### 📦 Backlog

##### T5: Content Model Design
**Dependencies**: T2 (MCP Setup)

Design YAML content architecture supporting base + role-specific composition.

**Acceptance Criteria**:
- [ ] Create `content/base.yaml` with static fields (name, contact, education)
- [ ] Create `content/fragments/` directory structure
- [ ] Design fragment schema for: experience, skills, projects
- [ ] Document composition strategy in `docs/content-model.md`
- [ ] Create example fragments for 2-3 role types
- [ ] Validate all YAML against JSON Resume schema
- [ ] Write unit tests for composition logic

**File Structure**:
```
content/
├── base.yaml                 # Static: identity, contact, education
├── fragments/
│   ├── experience/
│   │   ├── goop.yaml
│   │   ├── no-borders.yaml
│   │   └── boiling-pot.yaml
│   ├── skills/
│   │   ├── full-stack.yaml
│   │   ├── leadership.yaml
│   │   └── ecommerce.yaml
│   └── roles/
│       ├── senior-engineer.yaml
│       ├── tech-lead.yaml
│       └── founder.yaml
```

---

##### T6: Composition Engine
**Dependencies**: T5 (Content Model)

Implement Python script to merge YAML fragments into valid JSON Resume.

**Acceptance Criteria**:
- [ ] Create `scripts/compose_resume.py`
- [ ] Implement YAML loading with validation
- [ ] Implement merge strategy for fragments
- [ ] Add JSON Resume schema validation
- [ ] Support role-specific composition via CLI args
- [ ] Handle merge conflicts gracefully
- [ ] Write comprehensive tests (pytest)
- [ ] Document usage in `docs/composition.md`

**CLI Interface**:
```bash
python compose_resume.py \
  --base content/base.yaml \
  --role content/roles/senior-engineer.yaml \
  --output build/resume.json \
  --validate
```

---

##### T7: PDF Generation CLI
**Dependencies**: T4 (Theme Freeze), T6 (Composition Engine)

Create unified CLI wrapper for the complete resume generation pipeline.

**Acceptance Criteria**:
- [ ] Create `scripts/build_resume.py`
- [ ] Integrate composition engine
- [ ] Call `resumed` with frozen theme
- [ ] Implement filename pattern: `{firstname}-{lastname}-{role}-{YYYYMMDD}.pdf`
- [ ] Add metadata injection (generation date, role key)
- [ ] Implement dry-run mode
- [ ] Add verbose logging
- [ ] Write integration tests

**CLI Interface**:
```bash
python build_resume.py \
  --role senior-engineer \
  --output artifacts/ \
  --validate \
  --verbose
```

**Output**: `james-valeii-senior-engineer-20251217.pdf`

---

##### T8: CI/CD Pipeline
**Dependencies**: T7 (PDF Generation CLI)

Automate validation and PDF generation on content changes.

**Acceptance Criteria**:
- [ ] Create GitHub Actions workflow (or equivalent)
- [ ] Run schema validation on YAML changes
- [ ] Build all role-specific PDFs
- [ ] Store PDFs as build artifacts
- [ ] Compare against baseline (visual regression)
- [ ] Fail pipeline on validation errors
- [ ] Document CI setup in `docs/ci-cd.md`

**Triggers**:
- Push to `main` branch
- Pull requests modifying `content/`
- Manual workflow dispatch

---

##### T9: MCP Integration & Testing
**Dependencies**: T2 (MCP Setup), T7 (PDF Generation)

Integrate MCP server with resume workflow for AI-assisted editing.

**Acceptance Criteria**:
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

##### T10: Documentation & Handoff
**Dependencies**: T9 (MCP Integration)

Create comprehensive documentation for the complete system.

**Acceptance Criteria**:
- [ ] Write `README.md` with quick start guide
- [ ] Document all CLI commands and options
- [ ] Create troubleshooting guide
- [ ] Document MCP integration patterns
- [ ] Write contribution guidelines
- [ ] Create architecture diagram
- [ ] Record demo video (optional)
- [ ] Publish to internal wiki/docs site

---

#### ✅ Complete

[No completed tasks yet.]

---

#### 🚫 Rejected

[No rejected tasks yet.]

---

## Notes & Decisions

### Font Management
- **Decision**: Vendor fonts in theme directory to prevent environment variation
- **Rationale**: Eliminates dependency on external CDNs and ensures deterministic builds
- **Implementation**: Copy EB Garamond WOFF2 files to `themes/valeii-professional/fonts/`

### Metadata Strategy
- **Decision**: Avoid visible generation timestamps in resume body
- **Rationale**: Prevents unnecessary PDF diffs and maintains clean presentation
- **Implementation**: Store metadata in PDF properties or separate JSON file

### Version Control
- **Decision**: Store generated PDFs in `artifacts/` with `.gitignore`
- **Rationale**: Keep repository clean, use CI for artifact distribution
- **Exception**: Store `baseline-resume.pdf` for visual regression testing

### Schema Validation
- **Decision**: Validate against official JSON Resume schema on every build
- **Rationale**: Ensures compatibility with all JSON Resume tools and themes
- **Implementation**: Use `ajv` or `jsonschema` library in validation step

---

## Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| Theme produces inconsistent PDFs | High | Freeze theme, test with content variations, use visual regression |
| MCP server incompatible with workflow | Medium | Test early (T2), maintain fallback manual editing process |
| JSON Resume schema changes | Low | Pin schema version, automate validation |
| Font rendering varies across environments | Medium | Vendor fonts locally, test on multiple OS |
| AI suggestions violate schema | Medium | Validate all changes before composition |

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
