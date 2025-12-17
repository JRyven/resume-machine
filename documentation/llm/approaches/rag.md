---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# LLM Retrieval-Augmented Generation (RAG)

## Basic RAG Approach

**Core Concept:** Index your code and retrieve only relevant snippets per query.

**Implementation:**
- Use vector databases (Chroma, FAISS) or lightweight alternatives
- Embed files and functions for semantic search
- Fetch only closely related code fragments for each prompt
- Prevents context window overflow with targeted retrieval

## Advanced: Two-Pass Retrieval (CGRAG)

**Problem:** Basic RAG misses context when queries lack specific keywords.

**Solution - Contextually-Guided RAG (CGRAG):**
1. Run initial RAG retrieval
2. Let LLM identify missing concepts from first pass
3. Re-run retrieval with LLM-generated keywords
4. Yields more precise context than single-pass retrieval

## Selective Retrieval for Performance

**Key Insight:** ~80% of code completions don't need cross-file context (Amazon Repoformer research).

**Optimization Strategy:**
- Train a small policy model to predict when retrieval helps
- Skip retrieval when not needed
- Results: ~70% faster completion with maintained accuracy

**Implementation:**
- Have LLM decide if query needs external context
- Use special token or simple classifier
- Only expand context when likely to improve output
