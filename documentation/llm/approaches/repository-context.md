---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# LLM Repository-Level Context Integration

## User Behavior Tracking

**Track Recent Activity:**
- Monitor files/functions recently opened or edited
- Provides clues about developer intent
- Include user-behavior snippets in context

**ContextModule Approach:**
- Retrieve similar code elsewhere in repository
- Fetch symbol definitions being used
- Append to prompt for improved relevance

## Similar Code Patterns

**Leverage Analogous Features:**
- Search for similar implementations in codebase
- Example: Use existing endpoint as reference for new endpoint
- Embed files and use semantic similarity search
- Discovers "code clones" that provide rich context

## Critical Dependencies

**Include Key Definitions:**
- Function definitions used in current code
- Configuration values (database schemas, API interfaces)
- Tag or index important symbols separately
- These often missed by keyword search alone

**Result:** Approximates "global view" without loading entire repository.
