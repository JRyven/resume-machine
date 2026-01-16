---
project_name: [PROJECT_NAME]
title: Writing Documentation - Content
description: Writing guidelines, clarity principles, and placeholder conventions for documentation.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [documentation, content, writing, style, placeholders]
---

# Documentation Content

**Path:** Documentation > Writing Documentation > Content

Guidelines for writing clear, consistent documentation content.

---

## Writing Principles

**Clarity First:**

- Be concise - remove unnecessary words
- Use active voice
- Define acronyms on first use
- Use examples to illustrate complex concepts

**Structure:**

- Start with the most important information
- Use progressive disclosure (overview → details)
- Group related concepts together
- End sections with actionable next steps

**Maintenance:**

- Write for future readers
- Include context that might not be obvious
- Update examples when code changes

---

## YAML Front Matter

All documentation files require YAML front matter:

```yaml
---
project_name: [PROJECT_NAME]
title: [DOCUMENT_TITLE]
description: [BRIEF_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: [X.X.X]
keywords: [[KEYWORD], [KEYWORD], [KEYWORD]]
---
```

**Field Requirements:**

- `project_name`: Project name or `[PROJECT_NAME]` placeholder
- `title`: Must match the H1 title in the document
- `description`: Concise summary (60-100 characters)
- `last_updated`: ISO 8601 date format
- `cleardoc_version`: Documentation system version
- `keywords`: Searchable terms as array

---

## Placeholder Format

Use bracket notation with SCREAMING_SNAKE_CASE for all placeholders:

```
[PROJECT_NAME]
[DOCUMENT_TITLE]
[BRIEF_DESCRIPTION]
[YYYY-MM-DD]
[KEYWORD]
```

**Rules:**

- Always use square brackets `[]`
- Use SCREAMING_SNAKE_CASE inside brackets
- Be descriptive: `[DATABASE_CONNECTION_STRING]` not `[VALUE]`

**Prohibited formats:**

- ❌ `{project_name}` (curly braces)
- ❌ `[project name]` (spaces)
- ❌ `<PROJECT_NAME>` (angle brackets)
- ❌ `__PROJECT_NAME__` (underscores)

---

## Breadcrumb Navigation

Include a breadcrumb path after the H1 title on subtopic files:

```markdown
# Document Title

**Path:** Documentation > [TOPIC] > [SUBTOPIC]
```

Breadcrumbs replace "Related Documentation" sections.
