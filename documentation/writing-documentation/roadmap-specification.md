---
project_name: Resume Machine
title: Writing Documentation - Roadmap Specification
description: Specification for project roadmap documentation structure and metadata.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [roadmap, specification, projects, tracking]
---

# Roadmap Specification

**Path:** Documentation > Writing Documentation > Roadmap Specification

Project tracking through a development lifecycle: In Progress, Backlog, Complete, Rejected.

## Lifecycle

Projects move through four stages:

1. **In Progress** - Exactly 0 or 1 project actively under development
2. **Backlog** - Projects planned for future work, ordered by priority
3. **Complete** - Finished projects with abbreviated documentation
4. **Rejected** - Abandoned projects with rationale preserved

---

## Structure

### Project Heading (H4)

```markdown
#### [PROJECT_NAME]
```

### Project Status (Note Enclosure)

Immediately following the project heading:

```markdown
'''
[Paragraph-form status information, context, and details]

Can include multiple paragraphs, code snippets, lists, and references.
'''
```

### Project Metadata

After the status section, include key-value pairs:

```markdown
created: [YYYY-MM-DD]
dependencies: [#prerequisite-project] | none
priority: low | medium | high
```

---

## Metadata Fields

**created:** ISO 8601 date when project was added

**dependencies:** Anchor links to prerequisite projects, or `none`

**priority:** One of: `low`, `medium`, `high`

---

## Anchor Links

---

## Metadata Requirements

Every project in In Progress or Backlog status must include the following metadata immediately after its status section:

```markdown
created: 2025-12-29
dependencies: [#anchor-to-project], [#another-project] or none
priority: low|medium|high
```

**Field Specifications:**

- `created`: Date in ISO 8601 format (2025-12-29) indicating when the project was added to the roadmap
- `dependencies`: Comma-separated list of markdown anchor links to other projects that must be completed before this project can be started. Use `none` if no dependencies exist
- `priority`: One of three values: `low`, `medium`, or `high`

Projects in Complete or Rejected status retain only:

- `created` date
- For Rejected projects: a `why: [explanation]` field describing the rejection rationale

### Markdown Anchor Link Format

Dependencies reference other projects using markdown anchor links. These are automatically generated from heading text:

- Convert heading text to lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Prepend with `#`

**Example:**

- Heading: `#### [User Authentication System]`
- Anchor: `#user-authentication-system`
- Reference: `dependencies: [#user-authentication-system]`

---

## Content Requirements

### Detail Retention by Status

The level of detail retained varies based on an item's lifecycle status:

**In Progress / Backlog Status:**

- Full descriptive text (1-2 sentence summaries plus optional additional paragraphs)
- All code examples in fenced code blocks
- All metadata fields
- Optional notes sections

**Complete Status:**

- Brief descriptive text only (1-2 sentences maximum)
- Metadata removed except `created` date
- Code examples removed (refer to version control logs)
- Notes sections removed

**Rejected Status:**

- Brief descriptive text explaining what was attempted
- All metadata removed except `created` date
- Single `why: [explanation]` field added to explain rejection rationale
- Code examples removed

### Code Examples and Notes Sections

Code examples and extended explanatory information may appear at the project level within the status section delimited by `'''`.

Projects may include a `### Notes` section to capture contextual information that doesn't belong in the status section.

---

## Simple Example

````markdown
# Project Roadmap

### In Progress

⚠️ LIMIT: Only 1 project allowed in this section

#### [User Authentication System]

'''
Building a secure JWT-based authentication system with role-based access control. Currently implementing the token generation and validation middleware.

```javascript
function generateTokens(userId, roles) {
  const accessToken = jwt.sign({ userId, roles }, process.env.JWT_SECRET, { expiresIn: '15m' });
  return { accessToken, refreshToken };
}
```
````

'''
created: 2025-10-15
dependencies: [#database-schema-setup]
priority: high

### Notes

Reference: https://jwt.io/introduction

### Backlog

#### [Real-time Notifications]

'''
Implement WebSocket-based notification system for real-time user updates.
'''
created: 2025-11-01
dependencies: none
priority: medium

#### [API Rate Limiting]

'''
Add rate limiting middleware to prevent abuse and protect service availability.
'''
created: 2025-11-05
dependencies: [#user-authentication-system]
priority: high

### Complete

#### [Database Schema Setup]

Set up relational database with initial schemas for users and projects.

created: 2025-09-15

### Rejected

#### [GraphQL API Implementation]

Attempted GraphQL API layer for more flexible client queries.

created: 2025-08-20
why: Team prioritized REST API stability. GraphQL adds complexity without clear benefit for current use cases. Revisit if client needs evolve.

```

---

## Best Practices

- **Keep status sections concise**: 1-3 paragraphs with optional code examples
- **Use In Progress limit**: Only 1 project actively being developed
- **Maintain dependencies**: Link to other projects using anchor references
- **Update regularly**: Keep descriptions current with project state
- **Strip details on completion**: Remove code examples and extended explanations when moving to Complete
- **Document rejections**: Explain why projects were rejected for future reference
```
