---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# Documentation Migration Prompt

Help me migrate this project's documentation from development phase to maintenance phase.

## Migration Tasks

### Progress Consolidation
- Move all completed milestone progress notes into a consolidated `## Progress Tracking` section in roadmap.md
- Ensure each completed milestone documents:
  - Detailed delivery notes
  - Success criteria verification
  - Metrics achieved
  - Known limitations
  - Next steps or follow-up items

### Documentation Restructuring
- Add a `## Maintenance Phase` section to roadmap.md
- Update the introduction to reflect the transition from "development project" to "maintained system"
- Preserve all historical development information
- Shift focus from development workflows to operations and maintenance
- Verify all cross-references remain valid after restructuring

## Documentation Standards

Follow these rules when extending documentation:

### File Organization
- Use flat directory structures with meaningful filenames
- Do NOT create new top-level files for the Documentation Index
- Extend existing top-level files listed in the Documentation Index
- Keep each file under ~4000 tokens for readability and AI context efficiency

### Content Structure
- Use proper Markdown headers (`#`, `##`, `###`) for clear hierarchy
- Include YAML metadata at the top of each file:
  ```yaml
  ---
  title: [Document Title]
  description: [Brief description]
  last_updated: 2025-12-17
  ---
  ```
- Make each file self-contained (readable without external context)
- Use frequent section headers to break content into logical chunks

### Handling Large Documents
When a document exceeds ~4000 tokens:
1. Create sub-files with descriptive names (e.g., `development-commands.md`, `development-documentation.md`)
2. Add a section index to the parent document
3. Update the Documentation Index to reflect the split

**Example split:**
- Original: `[Development Guide](/documentati../development/abstract.md)`
- Split into:
  - `[Development Guide](/documentati../development/abstract.md)` (overview + index)
  - `[Development Commands](/documentati../development/commands.md)`
  - `[Development Documentation](/documentati../development/documentation.md)`

### Content Best Practices
- Keep short examples inline; move long examples to separate files
- Provide both brief definitions and detailed explanations for new concepts
- Timestamp changes in planning documents (e.g., Roadmap)
- Mark task status clearly (e.g., Completed, In Progress, Planned)
- Link related documents with brief context explaining their relevance
- Maintain consistent sectioning across documents (e.g., Overview, Examples, References)

## Goal

Transform the documentation from a development roadmap to a comprehensive operations and maintenance guide for a stable, production system.
