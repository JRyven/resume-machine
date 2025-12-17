---
project_name: JSON CV
title: Documentation Content Standards
description: Best practices for writing clear, consistent, and maintainable documentation content
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, content, writing, standards, best-practices]
---

# Documentation Content Standards

This document covers the fundamental principles for creating high-quality documentation content, including writing guidelines and file organization standards.

---

## Content Best Practices

Follow these core principles to ensure your documentation is clear, useful, and maintainable:

- **Be as concise as possible** - Remove unnecessary words while maintaining clarity
- **Code comments explain "why" not "what"** (Clean Code principle) - Focus on reasoning and intent
- **Explain complex business logic with examples and usage patterns** - Use concrete examples to illustrate abstract concepts
- **Provide both brief definitions and detailed explanations for new concepts** - Start with the overview, then dive deep
- **Maintain consistent sectioning across documents** (e.g., Overview, Examples, References) - Use predictable structures
- **Use frequent section headers with proper Markdown headers** (`#`, `##`, `###`) for clear hierarchy to break content into logical chunks

### Writing Guidelines

**Clarity First:**
- Use active voice when possible
- Define acronyms on first use
- Avoid jargon unless your audience is technical
- Use examples to illustrate complex concepts

**Structure Matters:**
- Start with the most important information
- Use progressive disclosure (overview → details)
- Group related concepts together
- End with actionable next steps

**Maintenance Mindset:**
- Write for future readers, not just current understanding
- Include context that might not be obvious
- Update examples when code changes
- Review and refresh content regularly

---

## File Organization

Proper file organization ensures documentation is discoverable and maintainable.

### Directory Structure

Use this standard directory structure for documentation:

```
/docs/
├── dev/           # Developer documentation
│   ├── *.md       # Core development docs
│   └── ADRs/      # Architecture Decision Records
├── user/          # End-user documentation
│   └── *.md       # User guides and manuals
└── temp/          # Temporary or draft documentation
```

### File Naming Conventions

**General Rules:**
- Use kebab-case (lowercase with hyphens): `error-handling.md`, `testing-guide.md`
- Be specific and descriptive: `api-authentication.md` not `auth.md`
- For sub-files, use pattern: `[topic]-[subtopic].md`

**Examples:**
- ✅ `deployment-strategy.md` - Clear and specific
- ✅ `testing-coverage.md` - Follows sub-file pattern
- ❌ `stuff.md` - Too vague
- ❌ `MyDocument.md` - Uses incorrect casing

### Architecture Decision Records (ADRs)

**Location:** Store ADRs in `/docs/d../../architecture-decisions/` directory

**Naming Convention:** `[YYYYMMDD]-[feature]-[decision].md`
- `YYYYMMDD`: Date in ISO format
- `feature`: Brief feature or component name
- `decision`: Key decision made

**Examples:**
- `20251016-auth-oauth2.md`
- `20251020-database-postgresql.md`
- `20251025-api-versioning.md`

---

## Related Documentation

- [Documentation Guide (Index)](./documentation/abstract.md): Overview of all documentation standards
- [Documentation Metadata](./documentation/metadata.md): Front matter and file metadata standards
- [Documentation Structure](./documentation-structure.md): Header hierarchy and table of contents guidelines
