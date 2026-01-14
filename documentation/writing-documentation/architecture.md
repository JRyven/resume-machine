---
project_name: [PROJECT_NAME]
title: Writing Documentation - Architecture
description: Directory structure, file naming conventions, and header hierarchy for documentation.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [documentation, architecture, structure, naming, hierarchy]
---

# Documentation Architecture

**Path:** Documentation > Writing Documentation > Architecture

Rules governing documentation organization: directory structure, file naming, and header hierarchy.

---

## Directory Structure

Documentation uses a modular hierarchical system. Each topic has its own directory with an `abstract.md` index file.

```
documentation/
├── abstract.md            ← Root index
├── [TOPIC]/               ← Topic directory
│   ├── abstract.md        ← Topic index (mandatory)
│   ├── [SUBTOPIC].md      ← Detailed content
│   └── [SUBTOPIC].md      ← More detailed content
└── [TOPIC]/               ← Another topic
    └── ...
```

### Permitted Topics

Only the following top-level topic directories are permitted:

- architecture
- architecture-decisions
- code-style
- commands
- configuration
- data-schema
- deployment
- error-handling
- roadmap
- software-management
- testing
- user
- writing-documentation

### Directory Contents

**Mandatory:** `abstract.md` - Index and overview for the topic

**Optional:** Subtopic content files using descriptive kebab-case names

---

## File Naming

### Abstract Files

Every directory contains an `abstract.md` that introduces the topic and links to subtopic files.

### Content Files

Use descriptive kebab-case names:

- `architecture.md` - System architecture details
- `environment.md` - Development environment setup
- `configuration.md` - Configuration reference
- `style.md` - Code style guide
- `deployment.md` - Deployment procedures

**Rules:**
- Lowercase letters only
- Hyphens for word separation
- Descriptive and specific names
- Pattern for sub-files: `[TOPIC]-[SUBTOPIC].md`

**Examples:**
- ✅ `error-handling.md`
- ✅ `testing-coverage.md`
- ❌ `stuff.md` (too vague)
- ❌ `MyDocument.md` (wrong casing)

---

## Header Hierarchy

### Rules

```markdown
# Document Title (H1)
One H1 per document - the main title

## Major Section (H2)
Primary content divisions

### Subsection (H3)
Detailed breakdowns within major sections

#### Fine-Grained Detail (H4)
Use sparingly for necessary subdivisions
```

**Constraints:**
- One H1 per file (must match `title` in front matter)
- Sequential hierarchy (no skipping H2 → H4)
- Avoid H5 and H6 (split document instead)
- 3-8 H2 sections per document (ideal range)
- 2-5 H3 subsections per H2 section

---

## Linking

Use relative paths for all internal links:

```markdown
[Same directory](./file.md)
[Parent directory](../file.md)
[Subdirectory](subfolder/file.md)
[Section anchor](./file.md#section-name)
```

**Anchor format:** Convert header to lowercase, replace spaces with hyphens, remove special characters.

Example: `## Error Types` → `#error-types`
