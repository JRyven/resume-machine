---
project_name: [PROJECT_NAME]
title: Abstract Specification
description: Rules for creating abstract (index) files that introduce documentation topics.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [abstract, specification, documentation, index, standards]
---

# Abstract Specification

**Path:** Documentation > Writing Documentation > Abstract Specification

An abstract is an index file that introduces a documentation topic and links to detailed subtopic files.

## Purpose

Abstracts serve as entry points to documentation topics. They provide:

- Brief overview of the topic
- Key definitions and terminology
- Navigation links to detailed content
- Executive summary for quick reference

## Mandatory Sections

### YAML Front Matter

All abstracts must include YAML front matter with these fields:

```yaml
---
project_name: [PROJECT_NAME]
title: [TOPIC]
description: [BRIEF_TOPIC_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [[TOPIC], index, [KEYWORD]]
---
```

- `project_name`: Placeholder for project name
- `title`: Topic name (e.g., "Architecture", "Testing")
- `description`: 1-2 sentence description for AI scanning
- `last_updated`: ISO 8601 date format
- `cleardoc_version`: Semantic version number
- `keywords`: CSV list with topic name first, then related terms

### Main Heading

H1 heading matching the title YAML field.

### Executive Summary

Brief 2-3 sentence introduction explaining what the topic covers.

### Index Section

Navigation links to all subtopic files, one per line using markdown link format:

```markdown
## Index

[Subtopic One](./subtopic-one.md)
[Subtopic Two](./subtopic-two.md)
[Subtopic Three](./subtopic-three.md)
```

## Optional Sections

### Definitions

Define any domain-specific terminology, acronyms, or software-specific terms relevant to the topic. Include when topic uses specialized language.

## Content Structure Rules

- **No table of contents**: Avoid explicit TOC sections
- **No quick links**: Don't duplicate navigation in special "quick links" sections
- **No related documentation**: Navigation is breadcrumb-only (in content files, not abstracts)
- **No inline code**: Keep the abstract high-level
- **Single breadcrumb**: If needed, show path to parent only (not in abstracts typically)
- **Minimal examples**: None in abstract, leave for specification/template files

## Example

```markdown
---
project_name: [PROJECT_NAME]
title: Configuration
description: Standards and patterns for system and application configuration management.
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [configuration, index, standards, environment]
---

# Configuration

Comprehensive guide to managing configuration across development, testing, and production environments.

## Executive Summary

Configuration management ensures consistent behavior across environments while protecting sensitive data. This topic covers environment variables, configuration files, secrets management, and validation patterns.

## Definitions

- **Configuration**: Settings that change behavior without code changes
- **Secrets**: Sensitive values like API keys, passwords, database credentials
- **Environment Variables**: Key-value pairs passed to application at runtime
- **Configuration Profile**: Named set of configuration values for specific environment

## Index

[Configuration Reference](./configuration.md)
[Secrets Management](./secrets.md)
[Environment Setup](./environment.md)
```

## Size Guidelines

- Total: 250-400 words
- YAML: ~50 words
- Executive Summary: 30-50 words
- Definitions (optional): 50-100 words
- Index: Remaining words (usually short)
