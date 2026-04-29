---
project_name: Resume Machine
title: Reference Specification
description: Rules for creating reference documentation providing concise information lookup.
last_updated: [2026-04-29]
cleardoc_version: 2.3.0
keywords: [reference, specification, documentation, lookup]
---

# Reference Specification

**Path:** Documentation > Writing Documentation > Reference Specification

Reference documentation provides concise, structured lookup information for specific topics without explanatory prose.

## Purpose

References serve as quick lookup resources:

- API documentation with parameter definitions
- Command-line interface flag references
- Configuration option lists
- Schema definitions
- Tool usage guides

## Structure

References use consistent, scannable formats. Avoid narrative prose; use structured lists, tables, or code blocks.

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: Resume Machine
title: [TOPIC] Reference
description: [BRIEF_REFERENCE_DESCRIPTION]
last_updated: [2026-04-29]
cleardoc_version: 2.3.0
keywords: [reference, [TOPIC], lookup]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > [TOPIC] > [REFERENCE_TITLE]
```

### H1 Heading

Reference title without "Reference" suffix.

## Format Requirements

### Use Tables for Structured Data

```markdown
| Field        | Type   | Required | Description         |
| ------------ | ------ | -------- | ------------------- |
| [FIELD_NAME] | string | Yes      | [FIELD_DESCRIPTION] |
| [FIELD_NAME] | number | No       | [FIELD_DESCRIPTION] |
```

### Use Definition Lists for Grouped Items

```markdown
**[OPTION_NAME]**
Description of what this option does. Include default values and constraints.

**[OPTION_NAME]**
Description of what this option does. Include default values and constraints.
```

### Use Code Blocks for Examples

```
[EXAMPLE_CODE_OR_OUTPUT]
```

### Use Inline Code for References

Wrap command names, parameters, and values in backticks: `[COMMAND_NAME]`, `[PARAMETER]`

## Content Structure Rules

- **No narrative prose**: Use imperative descriptions only
- **Consistent formatting**: Table rows or list items formatted identically
- **Complete coverage**: Don't omit edge cases or deprecations
- **Include defaults**: Always show default values for optional items
- **Explain constraints**: Note limits, requirements, or restrictions clearly
- **No cross-topic links**: Keep reference self-contained

## Example

```markdown
---
project_name: Resume Machine
title: Configuration Reference
description: Complete list of configuration options with descriptions and defaults.
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [reference, configuration, options, settings]
---

# Configuration Reference

**Path:** Documentation > Configuration > Configuration Reference

## Options

| Option            | Type   | Default  | Description                                         |
| ----------------- | ------ | -------- | --------------------------------------------------- |
| `DATABASE_URL`    | string | required | Connection string for primary database              |
| `LOG_LEVEL`       | string | `info`   | Logging verbosity: `debug`, `info`, `warn`, `error` |
| `MAX_CONNECTIONS` | number | `10`     | Maximum concurrent database connections             |
| `CACHE_TTL`       | number | `3600`   | Cache expiration time in seconds                    |

## Commands

**[COMMAND_NAME]**
Brief description of command purpose and usage.
```

[COMMAND_SYNTAX]

```

Options:
- `--[OPTION_NAME]` - Description of what option does
- `--[OPTION_NAME]` - Description of what option does
```

## Size Guidelines

- Total: 300-500 words
- YAML: ~40 words
- Breadcrumb: 5 words
- Content: Remaining words (structured data or lists)
