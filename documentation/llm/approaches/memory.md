---
project_name: JSON CV
title:
description:
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: []
---

# LLM Persistent Memory and Summaries

## Memory Layer Architecture

**Cross-Session Context:**
- Store embeddings of important information (discussions, design docs, code sections)
- Use vector database for semantic retrieval
- Summarize coding sessions (decisions, new modules)
- Retrieve topically relevant summaries on demand

## Hybrid Memory System

**Short-Term Memory:**
- Track immediate editing session
- Recent code changes or prompts

**Long-Term Memory:**
- Vector DB indexes: README, design docs, architectural diagrams
- Module summaries and user chat logs
- Query with current context as vector
- Returns conceptually related past information

## Summarization Strategy

**Rolling Summaries:**
- LLM generates summaries of large files or design rationale
- Compress large code into small paragraphs
- Far fewer tokens, retrieved quickly
- Example: One-paragraph overview of legacy module's purpose

**Benefits:**
- Maintains continuity without re-injecting old content
- LLM has persistent "notes" on your repository
- Semantic storage finds "conceptually similar" information
- Context accumulation over time
