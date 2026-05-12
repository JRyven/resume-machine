---
project_name: Resume Machine
title: Writing Documentation - Management
description: Guidelines for splitting large documents and maintenance workflows.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [documentation, management, maintenance, splitting]
---

# Documentation Management

**Path:** Documentation > Writing Documentation > Management

Guidelines for managing large documents and maintenance workflows.

---

## Splitting Large Documents

When a document exceeds ~4000 tokens, restructure it into an index + sub-files pattern.

### When to Split

- Document exceeds ~4000 tokens
- Multiple distinct topics in one file
- Difficult to navigate or maintain

### How to Split

**Step 1: Convert to Index**

Transform the original file into an `abstract.md` that:

- Provides high-level overview
- Links to all sub-files with descriptions

**Step 2: Create Sub-Files**

Extract detailed content into focused sub-files:

- Use naming pattern: `[SUBTOPIC].md`
- Each file covers ONE focused aspect
- Include YAML front matter
- Add breadcrumb path

**Step 3: Update References**

- Fix links pointing to the original file
- Add section anchors if linking to specific content

### Index vs Sub-File Content

**Index contains:**

- Overview (2-3 paragraphs max)
- Links to sub-files with descriptions

**Index does NOT contain:**

- Detailed explanations
- Step-by-step tutorials
- Code examples longer than 5 lines

**Sub-files contain:**

- Detailed explanations
- Step-by-step guides
- Code samples
- Breadcrumb to parent

---

## Maintenance

### Update Checklist

When modifying documentation:

- [ ] Update `last_updated` field
- [ ] Verify internal links still work
- [ ] Check code examples are current
- [ ] Update breadcrumb if file moved

### Quality Checklist

- [ ] Front matter complete
- [ ] All links functional
- [ ] Headers follow hierarchy
- [ ] Content is concise
- [ ] No spelling errors
