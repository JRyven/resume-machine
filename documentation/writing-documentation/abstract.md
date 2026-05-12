---
project_name: Resume Machine
title: Writing Documentation
description: Standards and templates for creating and maintaining project documentation.
last_updated: 2026-01-04
cleardoc_version: 2.3.0
keywords: [documentation, standards, templates, writing]
---

# Writing Documentation

Standards for creating consistent, maintainable documentation across all project topics.

## Executive Summary

All documentation follows a modular hierarchical structure. Each topic directory contains an `abstract.md` index file and subtopic content files. Documents use YAML front matter for metadata, kebab-case file naming, and consistent header hierarchy. Content emphasizes clarity and conciseness over exhaustive specification.

**Core Principles:**

- One `abstract.md` index per directory
- YAML front matter on all files
- Kebab-case file naming
- H1 → H2 → H3 → H4 header progression (no skipping)
- Breadcrumb navigation over inline cross-references

## Definitions

**Abstract:** An index file (`abstract.md`) that introduces a topic directory and links to its subtopic files.

**Subtopic:** A detailed content file within a topic directory covering a specific aspect.

**Front Matter:** YAML metadata block at the top of every documentation file.

**Breadcrumb:** Navigation path showing document location in hierarchy (e.g., Documentation > Architecture > Environment).

## Index

[Specifications and Templates](./specifications-and-templates.md) - Complete system with 11 document type pairs
[Architecture](./architecture.md) - Directory structure, file naming, header hierarchy
[Content](./content.md) - Writing guidelines, clarity principles, placeholder format
[Management](./management.md) - Splitting large documents, maintenance workflows
