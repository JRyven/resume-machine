---
project_name: Resume Machine
title: Development Guide (Index)
description: Index and overview of development documentation covering setup, workflow, standards, and best practices.
last_updated: 2026-05-12
cleardoc_version: 2.3.0
keywords: [development, index, guide, workflow, standards]
---

# Development Guide

This is the **central index** for all development-related documentation. Whether you're setting up your environment for the first time, learning the codebase architecture, or contributing new features, start here to find the right documentation.

**New here?** Start with [Understanding Documentation Structure](#understanding-documentation-structure) below, then move to [Getting Started](#getting-started).

---

## Understanding Documentation Structure

This documentation uses a **modular, hierarchical system** to organize information. Each topic has its own directory with an `abstract.md` index file.

**Quick Structure:**

```
documentation/
├── abstract.md            ← You are here (main index)
├── STRUCTURE.md           ← Guide to documentation organization
├── architecture/          ← Topic directory
│   ├── abstract.md        ← Topic index
│   ├── architecture.md    ← Detailed content
│   └── environment.md     ← More detailed content
├── testing/               ← Another topic
├── configuration/         ← Another topic
└── ... (more topics)
```

**To understand this organization:** Read [Documentation Writing Guide](./writing-documentation/structure.md)

## Hierarchy Pattern

Every documentation topic follows this hierarchical structure:

```
topic-directory/
├── abstract.md          ← Index & overview (mandatory)
├── subtopic1.md         ← Detailed content
├── subtopic2.md         ← Detailed content
└── subtopic3.md         ← Detailed content
```

### Level 0: Documentation Root

The root `documentation/` directory contains:

- `abstract.md` - Main index for all documentation
- `STRUCTURE.md` - This guide (shows how documentation is organized)
- Topic directories (organized by subject)

### Level 1: Topic Directories

Each topic (architecture, testing, configuration, etc.) gets its own directory:

```
documentation/
├── architecture/        ← Topic directory
├── testing/            ← Topic directory
├── configuration/      ← Topic directory
├── commands/           ← Topic directory
├── code-style/         ← Topic directory
└── ...
```

### Level 2: Topic Contents

Each topic directory contains:

**Mandatory:**

- `abstract.md` - Table of contents and topic overview

**Optional:**

- Topic-specific content files (e.g., `architecture.md`, `environment.md`)
- Organized by increasing specificity

---

## File Naming Convention

### abstract.md (Index Files)

Every directory level has an `abstract.md` that serves as:

- **Index** - Table of contents for that topic
- **Overview** - Executive summary and key concepts
- **Definitions** - Key terminology for the topic
- **Navigation** - Links to related topics and subtopics

### Content Files

Specific content files use descriptive, kebab-case names:

- `architecture.md` - System architecture details
- `environment.md` - Development environment setup
- `configuration.md` - Configuration reference
- `style.md` - Code style guide
- `testing.md` - Testing approach
- `deployment.md` - Deployment procedures

---

## Complete Structure Example

Here's the current documentation structure showing the hierarchy:

```
documentation/
│
├── abstract.md                          [LEVEL 1: Main index]
├── STRUCTURE.md                         [This guide]
│
├── architecture/                        [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   ├── architecture.md                  [System architecture details]
│   └── environment.md                   [Development environment]
│
├── testing/                             [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── testing.md                       [Testing guide]
│
├── configuration/                       [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── configuration.md                 [Config reference]
│
├── commands/                            [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── commands.md                      [Command reference]
│
├── code-style/                          [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── style.md                         [Style guide]
│
├── deployment/                          [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── deployment.md                    [Deployment guide]
│
├── error-handling/                      [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── error-handling.md                [Error handling guide]
│
├── software-management/                 [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── software-management.md           [Dependency management]
│
├── roadmap/                             [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   ├── roadmap.md                       [Development roadmap]
│   └── specification.md                 [Roadmap specification]
│
├── data-schema/                         [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── data-schema.md                   [Data structure guide]
│
├── architecture-decisions/              [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   ├── ard-template.md                  [ARD template]
│   └── ard-abstract.md                  [How to write ADRs]
│
├── writing-documentation/               [LEVEL 2: Topic]
│   └── abstract.md                      [Topic index]
│   └── ... [Content files for writing docs]
│
├── user/                                [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   ├── guide.md                         [User guide]
│   └── user-guide.md                    [Alternative guide format]
│
├── llm/                                 [LEVEL 2: Topic]
│   ├── abstract.md                      [Topic index]
│   └── ... [LLM-specific documentation]
│
└── common/                              [LEVEL 2: Topic]
    └── abstract.md                      [Shared resources]
```

---

## Navigation Patterns

### Breadcrumb Navigation

Each file should include a breadcrumb trail showing context:

```markdown
**Path:** Documentation > [Topic] > [Subtopic]
```

### Linking Pattern

Link from specific content back to the topic abstract:

```markdown
## Related Topics

- [Topic Overview](./abstract.md) - Overview and index
- [Related Topic](../related/abstract.md) - Link to other topics
```

### Cross-References

Use consistent link patterns:

- **Topic-level reference:** `[Architecture Overview](./abstract.md)`
- **Sibling file reference:** `[Architecture Details](./architecture.md)`
- **Parent reference:** `[Documentation Index](../abstract.md)`
- **Sibling topic reference:** `[Configuration Guide](../configuration/abstract.md)`

---

## Creating New Documentation

### Adding a New Topic

1. **Create directory** with kebab-case name

   ```bash
   mkdir documentation/new-topic
   ```

2. **Create abstract.md** (topic index)

   ```markdown
   ---
   title: New Topic Overview
   description: Summary of this topic
   ---

   # New Topic

   ## Table of Contents

   1. [Section One](#section-one)
   2. [Section Two](#section-two)

   ## Section One

   [Content...]

   ## Related Documentation

   - [Main Index](../abstract.md)
   ```

3. **Add content files** as needed

   ```bash
   touch documentation/new-topic/detailed-content.md
   ```

4. **Link from parent abstract.md**
   - Add section in parent's Table of Contents
   - Add link in Related Documentation section

### Adding Content to Existing Topic

1. **Create new content file** with descriptive name
2. **Update abstract.md** in topic directory
   - Add to Table of Contents
   - Add to Related Documentation section
3. **Update parent abstract.md** if new content changes topic structure

---

## Abstract.md Template

Each topic directory has an `abstract.md` following this pattern:

```markdown
---
project_name: Resume Machine
title: [Topic Name] Overview
description: Overview of [Topic Name] including structure and key resources
last_modified: 2025-12-17
cleardoc_version: 2.3.0
keywords: [keywords, for, this, topic]
---

# [Topic Name]

Brief introduction to this documentation topic.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Concepts](#key-concepts)
3. [Related Resources](#related-resources)
4. [Quick Links](#quick-links)

---

## Overview

Executive summary of this topic area.

---

## Key Concepts

### Concept 1

Definition and explanation.

### Concept 2

Definition and explanation.

---

## Related Resources

- [Resource One](./resource-one.md) - Description
- [Related Topic](../other-topic/abstract.md) - Link to other topics
- [Parent Index](../abstract.md) - Link back up

---

## Quick Links

- **New here?** Start with [Overview](#overview)
- **Looking for X?** See [Resource One](./resource-one.md)
- **Related:** [Other Topic](../other-topic/abstract.md)
```

---

## Benefits of Hierarchical Structure

### 1. **Modularity**

- Each topic is self-contained
- Easy to maintain independently
- Clear boundaries between topics

### 2. **Discoverability**

- Natural folder structure mirrors mental models
- Table of contents at each level
- Consistent link patterns

### 3. **Scalability**

- Add new topics without restructuring
- Add subtopics without changing existing links
- Scales with project growth

### 4. **Maintainability**

- Single responsibility per file
- Clear ownership (folder = topic owner)
- Easy to find what you need

### 5. **Accessibility**

- Works with file explorers
- Works with Markdown readers
- Works with VS Code outline view
- SEO-friendly for online docs

---

## Best Practices

### DO

- ✅ Use `abstract.md` as the index for each directory
- ✅ Use kebab-case for file and directory names
- ✅ Keep files focused on a single topic
- ✅ Update abstract.md when adding/removing files
- ✅ Use consistent metadata in frontmatter
- ✅ Link up to parent and across to siblings
- ✅ Use the table of contents pattern

### DON'T

- ❌ Use generic names like `index.md` (use `abstract.md`)
- ❌ Mix different topic areas in one file
- ❌ Create orphaned files without links
- ❌ Nest more than 2 levels deep (keep it flat)
- ❌ Break the hierarchical pattern
- ❌ Remove abstract.md files
- ❌ Use inconsistent metadata

---

## Migration from Flat Structure

If migrating from flat structure:

1. **Identify topic areas** from existing documents
2. **Create directories** for each topic
3. **Create abstract.md** in each directory
4. **Move related files** into topic directories
5. **Update all links** to reflect new structure
6. **Update main abstract.md** with new structure
7. **Test all links** to ensure navigation works

---

## Tools & Integration

### VS Code Integration

The folder structure works naturally with VS Code:

- File explorer shows hierarchy
- Breadcrumb navigation available
- Outline view shows structure
- Search works across directories

### Static Site Generators

This structure converts well to:

- Hugo
- Jekyll
- Docusaurus
- MkDocs
- Vuepress

The `abstract.md` files become natural `index.md` files for site generation.

### Obsidian Integration

Perfect for Obsidian knowledge bases:

- Each folder is a workspace
- abstract.md is the folder note
- Backlinks work across hierarchies
- Graph view shows structure

---

## Summary

The CLEAR Docs hierarchical structure provides:

| Feature                  | Benefit                    |
| ------------------------ | -------------------------- |
| **Modular organization** | Easy to maintain and scale |
| **Consistent pattern**   | Intuitive to navigate      |
| **Clear hierarchy**      | Natural mental model       |
| **Abstract.md indexing** | Self-documenting structure |
| **Flexible linking**     | Works with many tools      |

Following this pattern ensures documentation stays organized, accessible, and maintainable as your project grows.

---
