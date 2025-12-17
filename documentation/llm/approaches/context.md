---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# LLM Context Management Best Practices

## Overview

Effective context management is crucial for getting high-quality responses from LLMs. This guide covers strategies for providing relevant context without exceeding token limits.

## Context Window Management

### Token Limits
- GPT-4: 8,192 tokens (input) + 4,096 (output)
- GPT-3.5: 4,096 tokens total
- Local models: Vary by model (4K-32K typical)

### Context Budgeting
- Reserve 20-30% for response generation
- Prioritize high-value context (recent code, related functions)
- Use summarization for historical context

## Context Types

### 1. Code Context
**What to include:**
- Current file being edited
- Directly imported/used functions
- Related class definitions
- Recent changes in the same module

**What to exclude:**
- Entire codebase
- Unrelated files
- Generated code (build artifacts)

### 2. Project Context
**Essential information:**
- Project structure overview
- Key architectural decisions
- Technology stack
- Coding conventions

### 3. Task Context
**Current work:**
- Specific task requirements
- Acceptance criteria
- Previous attempts/solutions
- Error messages

## Best Practices

### 1. Selective Inclusion
- Use RAG to fetch only relevant code snippets
- Include function signatures over full implementations
- Provide class hierarchies instead of all methods

### 2. Progressive Disclosure
- Start with high-level overview
- Add details as needed
- Use follow-up questions for clarification

### 3. Context Refreshing
- Update context when switching tasks
- Clear irrelevant context between sessions
- Use persistent memory for long-term knowledge

### 4. Prompt Engineering
- Be specific about what you need
- Provide examples of desired output format
- Include error context when debugging

## Tools and Techniques

### VS Code Integration
- Keep relevant files open
- Use GitHub Copilot for inline suggestions
- Leverage workspace context automatically

### External Tools
- Vector databases for code indexing
- Code graph databases for structural queries
- Summarization tools for large documents

## Common Pitfalls

### Over-Contexting
- Including too much irrelevant information
- Forgetting to update context for new tasks
- Not prioritizing current work over historical code

### Under-Contexting
- Assuming LLM knows project specifics
- Not providing error messages or stack traces
- Missing architectural constraints

## Metrics for Success

- Response relevance (80%+ directly useful)
- Error reduction in generated code
- Time saved vs manual implementation
- User satisfaction with suggestions
