---
project_name: JSON CV
title: Documentation Metadata Standards
description: Standards for YAML front matter, file metadata, and document organization
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, metadata, front-matter, yaml, organization]
---

# Documentation Metadata Standards

This document defines the standards for document metadata, including YAML front matter configuration and field specifications for consistent document organization and discoverability.

---

## Front Matter Configuration

All documentation files should include YAML front matter at the top to enable better organization, search capability, and automated tooling.

### Required Fields

```yaml
---
project_name: JSON CV
title: [DOCUMENT_TITLE]
description: [BRIEF_DESCRIPTION]
last_updated: 2025-12-17
---
```

### Optional Fields

Add these fields as needed to enhance metadata:

```yaml
---
project_name: JSON CV
title: [DOCUMENT_TITLE]
description: [BRIEF_DESCRIPTION]
last_updated: 2025-12-17
version: [SEMANTIC_VERSION]          # e.g., 1.0, 2.1.3
author: [AUTHOR_NAME]                # Primary maintainer
keywords: [tag1, tag2, tag3]             # Searchable keywords
status: [Active|Draft|Deprecated]    # Document lifecycle status
related_docs:                        # Structured related links
  - path: ./related-file.md
    description: Brief context
  - path: ../other/file.md
    description: Another related doc
---
```

### Field Descriptions

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `project_name` | String (Required) | Name of the project | `My Application` |
| `title` | String (Required) | Document title | `Architecture Overview` |
| `description` | String (Required) | One-line summary | `Clean architecture and layer breakdown` |
| `last_updated` | Date (Required) | ISO 8601 date | `2025-12-17` |
| `version` | String (Optional) | Semantic version | `1.0`, `2.1.3` |
| `author` | String (Optional) | Primary maintainer | `Jane Doe` |
| `tags` | Array (Optional) | Searchable keywords | `[architecture, clean-code, patterns]` |
| `status` | Enum (Optional) | Document state | `Active`, `Draft`, `Deprecated` |
| `related_docs` | Array (Optional) | Structured links | See example above |

### Best Practices

- **Always update `last_updated`** when making significant changes
- **Use consistent `project_name`** across all files (e.g., `JSON CV` placeholder for templates)
- **Keep `description` to one line** (60-100 characters)
- **Use `tags`** for cross-cutting concerns (e.g., `security`, `performance`, `api`)
- **Set `status: Draft`** for work-in-progress documents
- **Use `related_docs`** for structured cross-references (alternative to inline links)

### Field Validation

**Required Field Validation:**
- `project_name`: Must match project name or use `JSON CV` placeholder
- `title`: Must match the H1 title in the document
- `description`: Must be concise (60-100 characters) and descriptive
- `last_updated`: Must be valid ISO 8601 date format (2025-12-17)

**Optional Field Guidelines:**
- `version`: Use semantic versioning (MAJOR.MINOR.PATCH) for versioned documents
- `author`: Use for documents with specific maintainers
- `tags`: Use lowercase, hyphen-separated tags for consistency
- `status`: Use "Draft" for incomplete docs, "Deprecated" for outdated ones

---

## Metadata Usage

### Search and Discovery

Front matter enables powerful search and filtering capabilities:

- **Tag-based search**: Find all documents related to `security` or `api`
- **Status filtering**: Identify draft or deprecated documents
- **Author attribution**: Find documents maintained by specific team members
- **Version tracking**: Track document evolution alongside code versions

### Automated Processing

Metadata supports automated tooling:

- **Documentation generators**: Auto-build indexes and navigation
- **Link checkers**: Validate internal references
- **Content management**: Track document lifecycle and updates
- **Search indexing**: Enable full-text search with metadata filters

### Maintenance Automation

Use metadata for maintenance workflows:

- **Stale content detection**: Flag documents not updated in 6+ months
- **Review scheduling**: Prioritize draft documents for completion
- **Dependency tracking**: Identify documents affected by code changes
- **Quality metrics**: Track documentation completeness and coverage

---

## Related Documentation

- [Documentation Guide (Index)](./documentation/abstract.md): Overview of all documentation standards
- [Documentation Content](./documentation/content.md): Writing guidelines and file organization
- [Documentation Linking](./documentation/linking.md): Cross-referencing and navigation standards
