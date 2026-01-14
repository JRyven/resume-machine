---
project_name: [PROJECT_NAME]
title: Writing Documentation - Templates
description: Document templates for abstracts, subtopics, ADRs, and roadmaps.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [documentation, templates, abstract, adr, roadmap]
---

# Documentation Templates

**Path:** Documentation > Writing Documentation > Templates

Copy-paste templates for creating new documentation files.

---

## Abstract Template

Use for `abstract.md` index files in topic directories.

```markdown
---
project_name: [PROJECT_NAME]
title: [TOPIC]
description: [BRIEF_TOPIC_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: [X.X.X]
keywords: [[TOPIC], index, [KEYWORD]]
---

# [TOPIC]

[Brief introduction to the topic]

## Executive Summary

[Executive summary and key concepts]

## Definitions

[Key terminology for the topic - optional section]

## Index

[Subtopic One](./subtopic-one.md) - [Brief description]
[Subtopic Two](./subtopic-two.md) - [Brief description]
```

---

## Subtopic Template

Use for detailed content files within topic directories.

```markdown
---
project_name: [PROJECT_NAME]
title: [TOPIC] - [SUBTOPIC]
description: [BRIEF_SUBTOPIC_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: [X.X.X]
keywords: [[TOPIC], [SUBTOPIC], [KEYWORD]]
---

# [SUBTOPIC]

**Path:** Documentation > [TOPIC] > [SUBTOPIC]

[Brief introduction]

## Executive Summary

[Key points and overview]

## Definitions

[Key terminology - optional section]

[Remainder of content structured as appropriate for the topic]
```

---

## ADR Template

Use for Architecture Decision Records in `architecture-decisions/` directory.

**Naming:** `[YYYYMMDD]-[FEATURE]-[DECISION].md`

```markdown
---
project_name: [PROJECT_NAME]
title: [SHORT_TITLE]
description: [SHORT_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: [X.X.X]
keywords: [adr, architecture, [FEATURE]]
---

# ADR [NUMBER]: [SHORT_TITLE]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Deciders:** [LIST_OF_PEOPLE]

## Context

[Problem statement, constraints, requirements, stakeholders]

## Decision

[Chosen solution, key components, why this approach]

## Alternatives Considered

### Alternative 1: [NAME]
- **Description:** [BRIEF_EXPLANATION]
- **Pros:** [BENEFITS]
- **Cons:** [DRAWBACKS]
- **Reason for rejection:** [WHY_NOT_CHOSEN]

### Alternative 2: [NAME]
- **Description:** [BRIEF_EXPLANATION]
- **Pros:** [BENEFITS]
- **Cons:** [DRAWBACKS]
- **Reason for rejection:** [WHY_NOT_CHOSEN]

## Consequences

### Positive
- [BENEFIT_ONE]
- [BENEFIT_TWO]

### Negative
- [TRADEOFF_ONE]
- [TRADEOFF_TWO]

## Implementation Notes

[Files affected, dependencies, migration steps, testing considerations]

## Validation

[Success criteria, metrics to monitor, evaluation timeline]
```

---

## Roadmap Specification

For the complete roadmap system specification, see [Roadmap Specification](./roadmap-specification.md).

### Quick Reference

Roadmaps track projects through a lifecycle: In Progress → Backlog → Complete → Rejected.

**WIP Limits:**
- **Projects:** Maximum 1 in "In Progress"
- **Tasks:** Maximum 2 in "In Progress" per project

**Project metadata:**
- `created`: ISO 8601 date
- `dependencies`: Anchor links to prerequisite projects, or `none`
- `priority`: `low`, `medium`, or `high`

**Anchor format:** Convert heading to lowercase, spaces to hyphens, remove special characters.

Example: `#### [User Authentication]` → `#user-authentication`
