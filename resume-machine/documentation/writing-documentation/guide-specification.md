---
project_name: Resume Machine
title: Guide Specification
description: Rules for creating procedural guides that help users accomplish specific tasks.
last_updated: [2026-04-29]
cleardoc_version: 2.3.0
keywords: [guide, specification, documentation, procedural, tutorial]
---

# Guide Specification

**Path:** Documentation > Writing Documentation > Guide Specification

A guide provides step-by-step instructions to accomplish a specific task or goal, including context and explanation.

## Purpose

Guides help users:

- Complete specific tasks from start to finish
- Understand prerequisites and requirements
- Troubleshoot common issues
- Learn workflows through example
- Set up environments or systems

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: Resume Machine
title: [TOPIC] - [TASK] Guide
description: [BRIEF_GUIDE_DESCRIPTION]
difficulty: [Beginner|Intermediate|Advanced]
estimated_time: [TIME_ESTIMATE]
last_updated: [2026-04-29]
cleardoc_version: 2.3.0
keywords: [guide, [TOPIC], [TASK], [KEYWORD]]
---
```

- `difficulty`: Estimated complexity for target audience
- `estimated_time`: Expected completion time (e.g., "15 minutes", "1 hour")

### Breadcrumb Navigation

```markdown
**Path:** Documentation > [TOPIC] > [TASK] Guide
```

### Executive Summary

Brief 1-2 sentence description of what the guide teaches and the end goal.

### Prerequisites

List requirements before starting:

- Required tools or software and versions
- Required knowledge or skills
- Required access or permissions
- Required files or configuration

## Content Structure

### Step-by-Step Instructions

Number each major step. Within steps, use sub-bullets for details:

```markdown
1. **[Step Description]**

   - Detail or sub-step
   - Detail or sub-step with more specifics

2. **[Step Description]**
   - Detail or sub-step
```

### Code Blocks and Examples

Include real examples with language identifiers:

````markdown
**Command:**

```bash
[ACTUAL_COMMAND_TO_RUN]
```
````

**Output:**

```
[EXPECTED_OUTPUT]
```

````

### Verification Steps

After key steps, include how to verify success:

```markdown
**Verify:** Run `[VERIFICATION_COMMAND]` and confirm output contains `[EXPECTED_TEXT]`
````

### Screenshots or Examples

Describe what the user should see at each step.

## Optional Sections

### Troubleshooting

Common problems and solutions:

**Problem:** [SYMPTOM]
Solution: [RESOLUTION]

### Next Steps

Links to related guides or advanced topics.

## Example

````markdown
---
project_name: Resume Machine
title: Database - PostgreSQL Setup Guide
description: Step-by-step guide to installing and configuring PostgreSQL for development.
difficulty: Intermediate
estimated_time: 30 minutes
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [guide, database, postgresql, setup]
---

# PostgreSQL Setup Guide

**Path:** Documentation > Database > PostgreSQL Setup Guide

Set up PostgreSQL database for development and testing environments.

## Prerequisites

- macOS or Linux (Windows requires WSL)
- Administrator access to system
- 2GB available disk space
- Basic command-line familiarity

## Installation

1. **Install PostgreSQL**

   macOS:

   ```bash
   brew install postgresql@15
   ```
````

Linux (Ubuntu/Debian):

```bash
sudo apt-get install postgresql-15
```

2. **Verify Installation**

   ```bash
   psql --version
   ```

   Verify output shows: `psql (PostgreSQL) 15.X`

3. **Start PostgreSQL Service**

   macOS:

   ```bash
   brew services start postgresql@15
   ```

   Linux:

   ```bash
   sudo systemctl start postgresql
   ```

## Configuration

1. **Create Development Database**

   ```bash
   createdb [DATABASE_NAME]
   ```

2. **Connect to Database**

   ```bash
   psql [DATABASE_NAME]
   ```

   You should see the PostgreSQL prompt: `[DATABASE_NAME]=#`

## Troubleshooting

**Problem:** `psql: error: connection refused`
Solution: Ensure PostgreSQL service is running with `brew services list` (macOS) or `systemctl status postgresql` (Linux)

**Problem:** `createdb: error: could not connect to database template1`
Solution: Restart PostgreSQL service and try again

```

## Size Guidelines

- Total: 400-800 words
- YAML: ~50 words
- Breadcrumb: 5 words
- Executive Summary: 20-30 words
- Prerequisites: 40-60 words
- Steps: Remaining words
```
