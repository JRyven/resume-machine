---
project_name: [PROJECT_NAME]
title: Specifications and Templates
description: Complete documentation system with 11 document type specifications and templates.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [specifications, templates, documentation, standards]
---

# Specifications and Templates

**Path:** Documentation > Writing Documentation > Specifications and Templates

Complete specification and template pairs for 11 document types used throughout documentation.

Each document type includes:
- **Specification**: Rules and requirements for the document type
- **Template**: Copy-paste example showing format with placeholders

---

## Abstract

Index files that introduce documentation topics and link to subtopics.

[Abstract Specification](./abstract-specification.md) — Rules for creating abstract (index) files
[Abstract Template](./abstract-template.md) — Copy-paste template for new abstracts

---

## Subtopic

Detailed content files within a documentation topic covering specific concepts.

[Subtopic Specification](./subtopic-specification.md) — Rules for detailed content files
[Subtopic Template](./subtopic-template.md) — Copy-paste template for new subtopics

---

## Architecture Decision Record (ADR)

Documents for major architectural decisions, alternatives considered, and rationale.

[ADR Specification](./adr-specification.md) — Rules for ADR format and structure
[ADR Template](./adr-template.md) — Copy-paste template for new ADRs

---

## Reference

Quick-lookup documentation for commands, options, parameters, and configurations.

[Reference Specification](./reference-specification.md) — Rules for reference documentation
[Reference Template](./reference-template.md) — Copy-paste template for new references

---

## Guide

Step-by-step procedural guides for accomplishing specific tasks or workflows.

[Guide Specification](./guide-specification.md) — Rules for procedural guides
[Guide Template](./guide-template.md) — Copy-paste template for new guides

---

## Index

Organized collections of resources around a central theme, with multiple entry points and learning paths.

[Index Specification](./index-specification.md) — Rules for index documents
[Index Template](./index-template.md) — Copy-paste template for new indexes

---

## API Documentation

Endpoint documentation with parameters, request/response formats, and error codes.

[API Specification](./api-specification.md) — Rules for API documentation
[API Template](./api-template.md) — Copy-paste template for new API docs

---

## Roadmap

Project lifecycle tracking showing In Progress, Backlog, Complete, and Rejected projects.

[Roadmap Specification](./roadmap-specification.md) — Rules for roadmap structure
[Roadmap Template](./roadmap-template.md) — Copy-paste template for new roadmaps

---

## Unit Test Documentation

Standards and patterns for testing individual functions and components.

[Unit Test Specification](./unit-test-specification.md) — Standards for unit tests
[Unit Test Template](./unit-test-template.md) — Example unit tests with common patterns

---

## Integration Test Documentation

Standards and patterns for testing component interactions and multi-step workflows.

[Integration Test Specification](./integration-test-specification.md) — Standards for integration tests
[Integration Test Template](./integration-test-template.md) — Example integration tests with patterns

---

## Configuration Documentation

Configuration options, methods, validation rules, and environment-specific settings.

[Configuration Specification](./configuration-specification.md) — Rules for configuration docs
[Configuration Template](./configuration-template.md) — Copy-paste template for new config docs

---

## Using These Templates

1. **Choose a document type** based on what you're documenting
2. **Copy the template** file content
3. **Replace all `[PLACEHOLDERS]`** with your actual content (use `[SCREAMING_SNAKE_CASE]` format for values you want to vary)
4. **Reference the specification** if you need clarification on requirements
5. **Maintain consistency** across all documents using the same type

### Placeholder Format

All placeholders use `[SCREAMING_SNAKE_CASE]` format:
- `[PROJECT_NAME]` - Project identifier
- `[TOPIC_NAME]` - Topic name
- `[CONFIGURATION_VALUE]` - Configurable values
- `[FILE_PATH]` - File paths
- `[COMMAND_NAME]` - Commands to run
- `[ENDPOINT_PATH]` - API endpoint paths
