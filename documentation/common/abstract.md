---
project_name: JSON CV
title: Common Resources
description: Shared documentation resources and templates used across topics
last_modified: 2025-12-17
cleardoc_version: 2.3.0
keywords: [common, shared, resources, templates]
---

# Common Resources

This section contains shared documentation resources, templates, and utilities used across multiple documentation topics.

---

## Purpose

The `common/` directory serves as a central repository for:

- **Shared Templates** - Document templates used across topics
- **Common Definitions** - Glossary and terminology
- **Reusable Components** - Documentation patterns and snippets
- **Style Guides** - Markdown and formatting conventions
- **Shared Resources** - Assets used by multiple topics

---

## Contents

### Templates

- [Document Template](./templates/) - Standard document template
- [FAQ Template](./templates/) - FAQ section template
- [README Template](./templates/) - README template

### Definitions & Glossary

- [Glossary](./glossary.md) - Project-wide terminology
- [Acronyms](./acronyms.md) - Common acronyms and abbreviations

### Style & Conventions

- [Markdown Guide](./markdown-style.md) - Markdown formatting conventions
- [Writing Style](./writing-style.md) - Project writing style guide
- [Naming Conventions](./naming-conventions.md) - How to name files, directories, concepts

### Reusable Snippets

- [Code Examples](./code-examples/) - Reusable code snippets
- [Common Patterns](./patterns.md) - Documentation patterns

---

## Using Common Resources

### Linking to Common Resources

From any documentation file:

```markdown
[Glossary](../common/glossary.md)
[Style Guide](../common/markdown-style.md)
[Code Examples](../common/code-examples/)
```

### Using Templates

Copy templates to your topic directory and customize:

```bash
cp documentation/common/templates/document-template.md \
   documentation/my-topic/my-document.md
```

---

## Best Practices

### DO

- ✅ Link to common definitions instead of repeating them
- ✅ Reference common templates when creating new documents
- ✅ Add new common resources for patterns used in multiple places
- ✅ Keep common resources up-to-date

### DON'T

- ❌ Duplicate definitions across topics
- ❌ Create topic-specific versions of shared resources
- ❌ Link to temporary or outdated resources

---

## Related Documentation

- [Documentation Index](../abstract.md) - Main documentation index
- [Documentation Structure](../STRUCTURE.md) - How documentation is organized
- [Writing Documentation](../writing-documentation/abstract.md) - How to write good docs
