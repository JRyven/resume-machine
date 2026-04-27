---
project_name: [PROJECT_NAME]
title: Index Specification
description: Rules for creating index documents that organize and link related resources.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [index, specification, documentation, navigation, organization]
---

# Index Specification

**Path:** Documentation > Writing Documentation > Index Specification

An index organizes multiple resources around a central theme, providing categorized navigation to related documentation, tools, and references.

## Purpose

Indexes serve as discovery points:

- Organize related documentation by category or use case
- Provide multiple entry points to content
- List external resources and tools
- Create learning paths for common workflows
- Establish taxonomy for complex topic areas

## Difference from Abstract

- **Abstract**: Introduces a single topic area with its own directory
- **Index**: Organizes content across multiple sources or topics

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: [TOPIC] Index
description: [BRIEF_INDEX_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [index, [TOPIC], organization, [KEYWORD]]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > [PARENT_TOPIC] > [INDEX_TITLE]
```

### H1 Heading

Index title without "Index" suffix.

### Executive Summary

Briefly describe what the index organizes and who should use it.

## Content Structure

### Categorized Resource Lists

Group related resources under descriptive category headings:

```markdown
## Getting Started

[Starting Resource One](./path/to/resource.md)
[Starting Resource Two](./path/to/resource.md)

## Advanced Topics

[Advanced Topic One](./path/to/resource.md)
[Advanced Topic Two](./path/to/resource.md)

## Tools and References

[Reference Resource](./path/to/reference.md)
[Tool Documentation](./external/url)
```

### Optional: Learning Paths

Define recommended reading sequences:

```markdown
## Learning Path: From Beginner to Advanced

1. [First Concept](./resource.md) - Foundation understanding
2. [Second Concept](./resource.md) - Building on foundations
3. [Advanced Pattern](./resource.md) - Complex applications
```

### Optional: Comparison Tables

For indexes comparing similar resources:

```markdown
| Resource                 | Best For   | Difficulty | Time    |
| ------------------------ | ---------- | ---------- | ------- |
| [Guide One](./guide1.md) | [USE_CASE] | Beginner   | 20 min  |
| [Guide Two](./guide2.md) | [USE_CASE] | Advanced   | 2 hours |
```

## Content Structure Rules

- **Clear categories**: Use consistent heading levels (H2 for categories, H3 for subcategories)
- **Brief descriptions**: Keep link text short; use parenthetical descriptions if needed
- **Consistent ordering**: Organize categories logically (basics to advanced, frequency of use, etc.)
- **Avoid duplication**: Each resource appears once; prefer hierarchical organization
- **External links**: Clearly mark external resources

## Example

```markdown
---
project_name: [PROJECT_NAME]
title: Development Resources Index
description: Comprehensive index of development guides, references, and tools organized by use case.
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [index, development, resources, organization]
---

# Development Resources Index

**Path:** Documentation > Development > Resources Index

Comprehensive guide to development resources, organized by task and topic area.

## Getting Started

[Development Environment Setup](./setup-guide.md)
[Project Structure Overview](./architecture/abstract.md)
[Running Tests Locally](./testing-guide.md)

## Core References

[API Reference](./api-reference.md)
[Configuration Reference](./configuration-reference.md)
[Command-Line Tools](./cli-reference.md)

## Common Workflows

[Deploying to Production](./deployment-guide.md)
[Database Migrations](./database-guide.md)
[Debugging Applications](./debugging-guide.md)

## Advanced Topics

[Performance Optimization](./optimization-guide.md)
[Security Hardening](./security-guide.md)
[Custom Extensions](./extensions-guide.md)

## Learning Path: Contributor to Maintainer

1. [Contribution Guidelines](./contributing.md) - How to start
2. [Code Review Standards](./code-review.md) - Quality expectations
3. [Architecture Decisions](./architecture-decisions/abstract.md) - System understanding
4. [Deployment Procedures](./deployment-guide.md) - Production operations
5. [Troubleshooting Guide](./troubleshooting.md) - Supporting others
```

## Size Guidelines

- Total: 300-500 words
- YAML: ~40 words
- Breadcrumb: 5 words
- Executive Summary: 20-40 words
- Content: Remaining words (categorized lists)
