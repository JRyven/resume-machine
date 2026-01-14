---
project_name: [PROJECT_NAME]
title: Subtopic Specification
description: Rules for creating detailed subtopic files within documentation topics.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [subtopic, specification, documentation, content]
---

# Subtopic Specification

**Path:** Documentation > Writing Documentation > Subtopic Specification

A subtopic is a detailed content file within a documentation topic that covers a specific aspect of the topic.

## Purpose

Subtopics provide focused explanations of individual concepts, procedures, or reference information. They follow a consistent structure for easy navigation and AI processing.

## Mandatory Sections

### YAML Front Matter

All subtopics must include YAML front matter:

```yaml
---
project_name: [PROJECT_NAME]
title: [TOPIC] - [SUBTOPIC]
description: [BRIEF_SUBTOPIC_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [[TOPIC], [SUBTOPIC], [KEYWORD], [KEYWORD]]
---
```

### Breadcrumb Navigation

Include a breadcrumb path immediately after the H1 heading:

```markdown
**Path:** Documentation > [TOPIC] > [SUBTOPIC]
```

### Main Heading

H1 heading matching the title YAML field, without the topic prefix.

### Executive Summary

Brief 1-2 sentence overview of what the subtopic covers.

### Content Sections

Organized hierarchically using H2-H4 headings (no H5 or deeper). Structure should match the information's logical flow.

## Optional Sections

### Definitions

Define specialized terminology specific to this subtopic if needed.

## Content Structure Rules

- **No table of contents**: Avoid explicit TOC sections
- **Consistent heading hierarchy**: H2 for major sections, H3 for subsections, H4 for details
- **Use code blocks**: Fenced blocks with language identifiers for all code examples
- **Include examples**: Real-world examples are encouraged to clarify concepts
- **Relative linking**: Link to sibling files using `[Name](./filename.md)` format
- **Breadcrumb only**: No "related documentation" sections, navigation through breadcrumbs

## Placeholder Format

All placeholders use `[SCREAMING_SNAKE_CASE]` format:
- `[PROJECT_NAME]` - Project identifier
- `[TOPIC_NAME]` - Topic name
- `[CONFIGURATION_VALUE]` - Configurable values
- `[FILE_PATH]` - File paths
- `[COMMAND_NAME]` - Commands to run

## Example

```markdown
---
project_name: [PROJECT_NAME]
title: Configuration - Environment Setup
description: Steps for configuring development and production environments.
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [configuration, environment, setup, development]
---

# Environment Setup

**Path:** Documentation > Configuration > Environment Setup

Guide to setting up configuration for development, staging, and production environments.

## Executive Summary

Each environment requires specific configuration values. Use environment files and variables to maintain environment-specific settings without code changes.

## Development Environment

Create a `.env.development` file in the project root:

```
API_URL=http://localhost:3000
DEBUG=true
LOG_LEVEL=debug
```

Load configuration at application startup using a configuration loader.

## Production Environment

Production requires additional security and monitoring configuration:

```
API_URL=https://api.example.com
DEBUG=false
LOG_LEVEL=error
ENABLE_MONITORING=true
```

## Validation

Always validate configuration on startup to catch missing or invalid values early.
```

## Size Guidelines

- Total: 400-800 words
- YAML: ~50 words
- Breadcrumb: 5 words
- Executive Summary: 20-40 words
- Content: Remaining words
