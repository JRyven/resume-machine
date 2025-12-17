---
project_name: JSON CV
title: Documentation Structure Standards
description: Standards for document structure, header hierarchy, and table of contents creation
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, structure, headers, hierarchy, table-of-contents]
---

# Documentation Structure Standards

This document defines standards for document structure, including header hierarchy rules and table of contents guidelines to ensure consistent and navigable documentation.

---

## Header Hierarchy Rules

Proper header hierarchy ensures logical document structure and enables automated table of contents generation.

### Hierarchy Rules

```markdown
# Document Title (H1)
Only one H1 per document - the main title at the top

## Major Section (H2)
Primary divisions of content

### Subsection (H3)
Detailed breakdowns within major sections

#### Fine-Grained Detail (H4)
Use sparingly - only for necessary subdivisions

##### Avoid H5 and H6
If you need this level, consider splitting the document
```

### Best Practices

- **One H1 per file**: The document title (after front matter)
- **Sequential hierarchy**: Don't skip levels (e.g., H2 → H4 without H3)
- **Descriptive headers**: Use clear, specific text (not "Introduction" or "Details")
- **Consistent casing**: Use Title Case or Sentence case consistently
- **Scannable structure**: Headers should allow quick skimming

### Header Guidelines

**H1 (Document Title):**
- Must match the `title` field in front matter
- Only one per document
- Placed immediately after front matter

**H2 (Major Sections):**
- 3-8 sections per document (ideal range)
- Represent the main organizational divisions
- Should be able to stand alone as major topics

**H3 (Subsections):**
- Break down H2 sections into manageable chunks
- 2-5 subsections per H2 section
- Focus on specific aspects of the major topic

**H4 (Details):**
- Use only when H3 sections need further subdivision
- Limit to 2-3 per H3 section
- Consider if content could be moved to a separate document

### Example Structure

```markdown
# Architecture Overview

## Overview
Brief introduction to the architecture

## Core Principles
### Separation of Concerns
Detailed explanation

### Dependency Inversion
Detailed explanation

## Layer Structure
### Domain Layer
What belongs in domain

### Data Layer
What belongs in data

### Presentation Layer
What belongs in presentation

## Design Patterns
### Repository Pattern
How we use repositories

### Factory Pattern
How we use factories

## Related Documentation
Links to related files
```

---

## Table of Contents Guidelines

For documents with multiple major sections (3+ H2 headers), include a table of contents.

### Auto-Generated TOC

Many Markdown renderers and editors auto-generate TOCs. For manual creation:

```markdown
## Table of Contents

1. [Overview](#overview)
2. [Core Principles](#core-principles)
3. [Layer Structure](#layer-structure)
4. [Design Patterns](#design-patterns)
5. [Related Documentation](#related-documentation)
```

### TOC Best Practices

- **Place after document title**: Immediately following the H1 and any introductory text
- **Link all H2 headers**: Include all major sections
- **Optionally include H3**: For longer documents, include subsections
- **Use numbered lists**: For linear reading (step-by-step guides)
- **Use bullet lists**: For reference documents (can read in any order)
- **Keep synchronized**: Update TOC when adding/removing sections

### When to Include TOC

**Include TOC when:**
- Document has 3+ H2 headers
- Content is longer than 1000 words
- Document serves as a reference guide
- Readers need to jump between sections frequently

### When to Skip TOC

**Skip TOC when:**
- **Short documents**: Fewer than 3 major sections
- **Single-topic files**: Documents with one clear focus
- **Index files**: Files that are already navigation hubs
- **Linear guides**: Step-by-step tutorials meant to be read sequentially

### TOC Maintenance

**Update Requirements:**
- Add new sections to TOC immediately
- Remove deleted sections from TOC
- Update anchor links if headers change
- Verify link accuracy after restructuring

**Automation:**
- Use tools that auto-generate TOC from headers
- Include TOC generation in documentation build process
- Validate TOC links in CI/CD pipelines

---

## Document Organization Patterns

### Reference Documents

**Structure for reference docs:**
- Overview section (optional)
- Alphabetically or logically grouped sections
- Consistent subsection patterns
- Comprehensive index or TOC

### Guide Documents

**Structure for guides:**
- Introduction with prerequisites
- Numbered steps or phases
- Examples and code samples
- Troubleshooting section
- Next steps or related guides

### Index Documents

**Structure for indexes:**
- Brief overview
- Organized list of links with descriptions
- Quick reference section
- Related documentation

### Decision Records

**Structure for ADRs:**
- Context and problem statement
- Proposed solution
- Alternatives considered
- Consequences and implementation

---

## Related Documentation

- [Documentation Guide (Index)](./documentation/abstract.md): Overview of all documentation standards
- [Documentation Content](./documentation/content.md): Writing guidelines and best practices
- [Documentation Formats](./documentation-formats.md): Specialized document templates and formats
