---
project_name: JSON CV
title: Documentation Management Standards
description: Standards for managing large documents, maintenance workflows, and using the documentation system
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, management, maintenance, large-documents, workflow]
---

# Documentation Management Standards

This document covers standards for managing large documents, maintenance workflows, and practical guidance for using the documentation system effectively.

---

## Handling Large Documents

### When to Split Documentation

Do NOT create new top-level files for the Documentation Index unless a file exceeds approximately **4000 tokens**.

When a document exceeds ~4000 tokens, restructure it into an **index pattern** with focused sub-files.

### How to Split: Index + Sub-Files Pattern

#### Step 1: Convert Main File to Index

Transform the original comprehensive document into an **index file** that:
- Retains the original filename (e.g., `testing.md`)
- Provides high-level overview of the topic
- Contains quick reference information (commands, key stats, etc.)
- Links to all sub-files with **descriptive headings** and **brief summaries**
- Includes a summary table or status section if applicable

#### Step 2: Create Focused Sub-Files

Extract detailed content into **sub-files** with clear, descriptive names:
- Use naming pattern: `[topic]-[subtopic].md` (e.g., `testing-guide.md`, `testing-coverage.md`)
- Each sub-file covers ONE focused aspect of the topic
- Include YAML front matter with descriptive title and description
- Add back-link to index file in overview section
- Cross-reference related sub-files in "Related Documentation" section

#### Step 3: Update Cross-References

- Update links in `/README.md` Documentation Index if needed
- Update references in other documents pointing to the original file
- Ensure all sub-files link back to the index
- Add "See also" or "For more details" references between related sub-files

### Split Pattern Examples

#### Example 1: Testing Documentation (Implemented)

**Before:** Single `testing.md` file (600+ lines)

**After:** Index + 4 focused sub-files
```
testing.md (INDEX - 132 lines)
├── testing-guide.md (Methodology: TDD, test types, best practices)
├── testing-structure.md (Organization: directories, naming, tooling)
├── testing-coverage.md (Metrics: goals, reporting, analysis)
└── test-summary.md (Status: current test breakdown)
```

**Index file structure:**
```markdown
# Testing Documentation

**Quick stats:** Total Tests: 90 | Status: ✅ | Coverage: High

## Overview
[Brief philosophy and approach]

### Quick Reference
[Common commands]

## Documentation Index

### [Testing Guide](./testing-guide.md)
**Brief description of what's in this sub-file**
- Bullet point of key topics covered
- Another key topic
- ...

### [Testing Structure](./testing-structure.md)
**Brief description**
- Key topics...

## [Summary section if applicable]
[Table or high-level metrics]

## Related Documentation
[Links to non-testing docs]
```

#### Example 2: Development Guide (Existing Pattern)

**Structure:**
```
dev-abstract.md (INDEX)
├── dev-commands.md (Terminal commands and workflows)
├── dev-code-style.md (Coding standards and conventions)
└── development.md (Setup and environment)
```

#### Example 3: Roadmap (Minimal Index)

**Structure:**
```
roadmap.md (MINIMAL INDEX - just links)
├── initial.md (Initial build stages)
└── maintenance.md (Long-term maintenance)
```

### Naming Conventions for Sub-Files

| Pattern | Example | Use Case |
|---------|---------|----------|
| `[topic]-[subtopic].md` | `testing-guide.md` | Standard sub-file |
| `[topic]-[aspect].md` | `testing-coverage.md` | Specific aspect of topic |
| `[topic]-[type].md` | `initial.md` | Different types/phases |

**Key principle:** Sub-file names should be **self-documenting** and **predictable**.

### What Belongs in Index vs. Sub-Files?

**Index file should contain:**
- ✅ High-level overview (2-3 paragraphs max)
- ✅ Quick reference (commands, shortcuts, key stats)
- ✅ Descriptive links to all sub-files with summaries
- ✅ Summary tables or at-a-glance status
- ✅ Cross-references to related documentation

**Index file should NOT contain:**
- ❌ Detailed explanations (move to sub-files)
- ❌ Step-by-step tutorials (move to sub-files)
- ❌ Comprehensive lists or tables (move to sub-files)
- ❌ Code examples longer than 5 lines (move to sub-files)

**Sub-files should contain:**
- ✅ Detailed explanations and examples
- ✅ Step-by-step guides and workflows
- ✅ Comprehensive reference information
- ✅ Code samples and implementation details
- ✅ Back-link to index in overview section

---

## How to Use This Documentation System

This section provides step-by-step guidance for common documentation tasks.

### Adding a New Document

1. **Determine the appropriate directory**:
   - `/docs/dev/` - Developer documentation (architecture, testing, deployment)
   - `/docs/user/` - End-user documentation (user guides, FAQs)
   - `/docs/d../../architecture-decisions/` - Architecture Decision Records
   - `/docs/temp/` - Temporary or draft documentation

2. **Choose a meaningful filename**:
   - Use kebab-case (lowercase with hyphens): `error-handling.md`, `testing-guide.md`
   - Be specific and descriptive: `api-authentication.md` not `auth.md`
   - For sub-files, use pattern: `[topic]-[subtopic].md`

3. **Add front matter** (see [Front Matter Configuration](#front-matter-configuration)):
   ```yaml
   ---
   project_name: JSON CV
   title: Your Document Title
   description: Brief one-line description
   last_updated: 2025-12-17
   keywords: [relevant, tags]
   ---
   ```

4. **Structure the content**:
   - Start with H1 title (matching front matter `title`)
   - Add table of contents if 3+ major sections
   - Use proper header hierarchy (H2 → H3 → H4)
   - Include "Related Documentation" section at bottom

5. **Link from other documents**:
   - Add link to `/README.md` Documentation Index if it's a top-level document
   - Add cross-references from related documents
   - Update index files if creating a sub-file

### Updating Existing Documentation

1. **Update the `last_updated` field** in front matter
2. **Review and update internal links** if file structure changed
3. **Check table of contents** is still accurate
4. **Verify code examples** still work
5. **Update version number** if using semantic versioning

### Creating an Index + Sub-Files Structure

When a document exceeds ~4000 tokens:

1. **Rename the main file** (if needed) to serve as index (e.g., `testing.md`)
2. **Create sub-files** following pattern: `[topic]-[subtopic].md`
3. **Move detailed content** from index to appropriate sub-files
4. **Update the index** with:
   - High-level overview
   - Quick reference information
   - Links to all sub-files with descriptions
   - Summary table or status section

5. **Update cross-references**:
   - Fix links in `/README.md`
   - Update references in other documents
   - Add back-links in sub-files to index
   - Add cross-references between related sub-files

See [Handling Large Documents](#handling-large-documents) for detailed guidelines.

### Writing Architecture Decision Records (ADRs)

1. **Copy the template**: `/docs/d../../architecture-decisions/TEMPLATE-ADR.md`
2. **Name the file**: `[YYYYMMDD]-[feature]-[decision].md` (e.g., `20251016-auth-oauth2.md`)
3. **Fill in all sections**: Context, Decision, Consequences, Alternatives
4. **Add to ADR index**: Update `/docs/d../../architecture-decisions/README.md`
5. **Link from relevant docs**: Reference the ADR in related technical documentation

### Maintaining Documentation Quality

**Regular Maintenance Tasks:**

- **Monthly**: Review `last_updated` dates, update stale content
- **Per Release**: Update version numbers, verify examples still work
- **Per Major Change**: Create or update ADRs, update architecture diagrams
- **Continuous**: Fix broken links, improve clarity, add examples

**Quality Checklist:**

- [ ] Front matter is complete and accurate
- [ ] All internal links work correctly
- [ ] Code examples are tested and current
- [ ] Headers follow hierarchy rules
- [ ] Table of contents is accurate (if present)
- [ ] Related documentation section is complete
- [ ] No spelling or grammar errors
- [ ] Content is concise and scannable
- [ ] Examples are clear and relevant

---

## Related Documentation

- [Documentation Guide (Index)](./documentation/abstract.md): Overview of all documentation standards
- [Documentation Content](./documentation/content.md): Writing guidelines and file organization
- [Documentation Metadata](./documentation/metadata.md): Front matter and metadata standards
