---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# LLM Practical Implementation Tips

## Code-Aware Chunking

**Logical Splitting:**
- Use AST-based splitters (e.g., LlamaIndex CodeSplitter)
- Keep functions and classes intact in chunks
- Break files at function boundaries
- Returns meaningful, complete code units

**Benefits:**
- Retrieval returns whole functions or classes
- Avoids fragmenting code into incoherent pieces
- LLM can answer "What does function X do?" correctly

## Efficient Retrieval Techniques

**Performance Optimization:**
- Simple similarity metrics can outperform complex embeddings
- Jaccard-over-symbols search: set overlap of identifiers
- Fast and "good enough" for most cases
- Balance accuracy and speed

**Implementation Options:**
- Quick on-disk index (SQLite full-text)
- Approximate nearest-neighbor on embeddings
- Choose based on size and hardware constraints

## High-Level Documentation

**Context Priming:**
- Write clear README or architecture overviews
- Provide textual "big picture" for domain
- Feed service/module summaries before specifics
- Grounds detailed answers in project intent

## VS Code Integration

**Leverage Built-in Features:**
- Keep relevant code files open/in focus
- Use comments or docstrings to highlight important parts
- Example: `/// Module X: handles user authentication`
- Primes LLM with module-level intent

## Iterative Refinement

**Continuous Improvement:**
- Monitor LLM outputs for context gaps
- Explicitly point to missing pieces
- Ask follow-up questions to drill down
- Adjust indexing/summaries based on frequent needs
- Combine retrieval with direct prompting
