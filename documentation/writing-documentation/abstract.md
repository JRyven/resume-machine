---
project_name: JSON CV
title: Documentation Guide (Index)
description: Index and overview of documentation standards, practices, and guidelines for creating and maintaining project documentation.
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [documentation, standards, guidelines, index, writing]
---

# Documentation Guide

This is the **central index** for all documentation-related standards and practices. Whether you're writing new documentation, maintaining existing files, or learning documentation best practices, start here to find the right guidelines and tools.

---

## Executive Summary

The Documentation Guide provides comprehensive standards for creating, organizing, and maintaining high-quality documentation. Key focus areas include consistent formatting, effective linking strategies, and scalable document structures. The guide emphasizes practical standards that improve discoverability and maintainability across all documentation files.

**Best Practices Checklist:**
- [ ] Include YAML front matter in all documentation files
- [ ] Use relative paths for internal links
- [ ] Follow header hierarchy rules (H1 → H2 → H3 → H4)
- [ ] Add "Related Documentation" sections to all files
- [ ] Update `last_updated` field when making changes
- [ ] Use descriptive link text with context
- [ ] Create ADRs for major technical decisions
- [ ] Split large documents when exceeding ~4000 tokens

---

## Table of Contents

1. [Quick Links](#quick-links)
2. [Getting Started](#getting-started)
3. [Core Documentation Topics](#core-documentation-topics)
4. [Related Documentation](#related-documentation)

---

## Quick Links

**Essential Commands:**
- Format check: `[FORMAT_CHECK_COMMAND]` (See [Commands Reference](../development/commands.md))
- Link validation: `[LINK_CHECK_COMMAND]`
- TOC generation: `[TOC_COMMAND]`

**Most Referenced Docs:**
- [Documentation Content](./documentation/content.md) - Writing guidelines and file organization
- [Documentation Metadata](./documentation/metadata.md) - Front matter and metadata standards
- [Documentation Linking](./documentation/linking.md) - Cross-referencing and navigation standards

---

## Getting Started

### For New Document Contributors

If you're new to contributing documentation, follow this recommended reading order:

1. **[Documentation Metadata](./documentation/metadata.md)** - Required metadata and YAML structure for all files
2. **[Documentation Content](./documentation/content.md)** - Writing guidelines and best practices
3. **[Documentation Structure](./documentation-structure.md)** - Document organization and formatting standards
4. **[Documentation Linking](./documentation/linking.md)** - Creating effective cross-references and navigation
5. **[Documentation Management](./documentation-management.md)** - Practical guides for using the documentation system
6. **[How to Use This Documentation System](./documentation.md#how-to-use-this-documentation-system)** - Step-by-step guides for common tasks

### Quick Start Checklist

- [ ] Review [Documentation Metadata](./documentation/metadata.md) and add to new files
- [ ] Read [Documentation Content](./documentation/content.md) before writing
- [ ] Study [Documentation Linking](./documentation/linking.md) for cross-references
- [ ] Follow [Documentation Structure](./documentation-structure.md) for organization
- [ ] Add "Related Documentation" section to all files
- [ ] Update `last_updated` field when making changes

---

## Core Documentation Topics

### Standards & Best Practices

**[Documentation Content](./documentation/content.md)**
Core principles for writing clear, consistent, and maintainable documentation content, including file organization standards.

**[Documentation Metadata](./documentation/metadata.md)**
Standards for YAML front matter, file metadata, and document organization for better search and automation.

### Structure & Formatting

**[Documentation Linking](./documentation/linking.md)**
Standards for internal linking, cross-referencing, and navigation to ensure documentation connectivity.

**[Documentation Structure](./documentation-structure.md)**
Standards for document structure, header hierarchy, and table of contents creation for consistent organization.

**[Documentation Formats](./documentation-formats.md)**
Templates and structures for specialized document types like roadmaps, ADRs, and API documentation.

### Document Management

**[Documentation Management](./documentation-management.md)**
Guidelines for managing large documents, maintenance workflows, and practical usage of the documentation system.

### Decision Records

**[ADRs README](../../architecture-decisions/README.md)**
Guidelines for creating and maintaining Architecture Decision Records.

**[ADR Template](../../architecture-decisions/TEMPLATE-ADR.md)**
Standard template for documenting major technical decisions.

---

## Related Documentation

- [README](../../README.md): Project overview and main documentation index
- [Dev Guide: Abstract](../development/abstract.md): Development documentation overview
- [Abstract Template](./documentation-template-for-abstracts.md): Guidelines for creating index/abstract documents
- [User Guide](../user/guide.md): End-user documentation standards
