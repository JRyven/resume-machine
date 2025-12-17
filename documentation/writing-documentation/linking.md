---
project_name: JSON CV
title: Documentation Linking Standards
description: Standards for internal linking, cross-referencing, and navigation in documentation
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, linking, navigation, cross-references, markdown]
---

# Documentation Linking Standards

This document defines standards for creating effective internal links, cross-references, and navigation to ensure documentation is interconnected and discoverable.

---

## Internal Linking Standards

Consistent internal linking improves navigation and maintains documentation integrity.

### Linking Format

Use **relative paths** for all internal links:

```markdown
<!-- Good: Relative path -->
[Architecture Overview](./architecture.md)
[User Guide](../user/guide.md)
[Root README](../../README.md)

<!-- Bad: Absolute paths -->
[Architecture](/docs/dev/architecture.md)
[User Guide](/Users/username/project/docs/user/guide.md)
```

### Path Guidelines

**Relative Path Rules:**
- `./file.md` - Same directory
- `../file.md` - Parent directory
- `../../file.md` - Grandparent directory
- `subfolder/file.md` - Subdirectory

**Directory Structure Awareness:**
- Links should work regardless of where the documentation is hosted
- Avoid absolute paths that break when documentation is moved
- Test links after restructuring documentation

### Anchor Links

Link to specific sections within documents:

```markdown
[Error Types](./error-handling.md#error-types)
[API Endpoints](./api-reference.md#authentication)
[Best Practices](./testing-guide.md#test-organization)
```

**Anchor Format:**
- Convert header text to lowercase
- Replace spaces with hyphens
- Remove special characters
- Example: `## Error Types` → `#error-types`

---

## Adding Context to Links

Always provide context when linking to help readers understand relevance:

### Good Examples

```markdown
<!-- Good: Context provided -->
See [Testing Guide](./testing-guide.md) for TDD methodology and best practices.
For deployment instructions, refer to [Deployment Guide](./deployment.md).

<!-- Acceptable: Brief inline context -->
Review the [Architecture Overview](./architecture.md) before proceeding.
```

### Poor Examples

```markdown
<!-- Bad: No context -->
See [this document](./testing-guide.md).
Click [here](./deployment.md).
Read [more](./architecture.md).
```

### Context Guidelines

- **Explain relevance**: Why should the reader follow this link?
- **Set expectations**: What will they find at the destination?
- **Use descriptive text**: Make link text meaningful without context
- **Keep it concise**: Don't make descriptions overly long

---

## Related Documentation Section

Include a **Related Documentation** section at the bottom of each file:

```markdown
## Related Documentation

- [README](../../README.md): Project overview and documentation index
- [Architecture Overview](./architecture.md): System design and layer structure
- [Testing Guide](./testing-guide.md): TDD methodology and best practices
- [Deployment](./deployment.md): Deployment options and instructions
```

### Related Documentation Best Practices

**Content Guidelines:**
- Include 3-5 related documents maximum
- Start with the most important/related documents
- Provide brief descriptions (1-2 sentences) for each link
- Group by relationship type when appropriate

**Ordering Priority:**
1. Parent index documents
2. Directly related technical documents
3. Supporting reference materials
4. Related processes or workflows

**Maintenance:**
- Update when new related documents are created
- Remove links to deleted or significantly changed documents
- Review periodically for relevance

---

## Cross-Reference Best Practices

### Bidirectional Linking

- **Link forward and backward**: If File A references File B, consider adding a back-link from File B to File A
- **Maintain consistency**: Ensure reciprocal links stay synchronized
- **Use appropriate link text**: Different text for forward vs. backward links

### Link Maintenance

- **Use descriptive link text**: Avoid "click here" or generic phrases
- **Check links regularly**: Use automated tools or manual checks to verify link integrity
- **Update after restructuring**: Fix broken links when files are moved or renamed
- **Link to specific sections**: Use anchor links when referencing specific content

### Link Types

**Navigation Links:**
- Table of contents entries
- Index page links
- Section cross-references

**Reference Links:**
- API documentation references
- External resource citations
- Related specification documents

**Contextual Links:**
- "See also" references
- Alternative approach links
- Prerequisite document links

---

## Link Validation

### Manual Checking

**Periodic Review Process:**
1. Check all links in recently updated documents
2. Validate anchor links exist and are correct
3. Test relative paths from different directory levels
4. Verify external links are still accessible

### Automated Tools

**Recommended Tools:**
- Markdown link checkers (e.g., `markdown-link-check`)
- Documentation generators with link validation
- CI/CD pipeline link checking
- IDE extensions for broken link detection

### Common Issues

**Broken Links:**
- Files moved or renamed without updating references
- Anchor links pointing to non-existent headers
- Case sensitivity issues in file paths

**Outdated Context:**
- Link descriptions no longer accurate
- Related documents no longer relevant
- Changed document purposes or scopes

---

## Related Documentation

- [Documentation Guide (Index)](./documentation/abstract.md): Overview of all documentation standards
- [Documentation Structure](./documentation-structure.md): Header hierarchy and organization standards
- [Documentation Management](./documentation-management.md): Large document handling and maintenance
