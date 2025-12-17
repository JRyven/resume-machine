# CLEARDocs Template System

A lean, highly-structured template framework for project documentation, configuration, and organization.

## What Is This?

**cleardocs-template-system** is a standardized blueprint deployed to your project. It provides:

- Complete documentation structure (user guides, dev docs, architecture, ADRs, LLM integration)
- Consistent metadata and frontmatter standards
- Pre-built navigation and indexing
- Example structures for source code, tests, and configuration

## How It Works

When you instantiate this template in your project:

1. Copy this entire directory to your target project
2. Run initialization tools to substitute placeholders (`JSON CV`, `2025-12-17`, etc.)
3. Customize `src/`, `tests/`, `config/`, `common/` for your project type
4. Start with `documentation/abstract.md` as your deployed project guide

## Key Directories

**`documentation/`** — The heart of the template. Deploy this to your project as-is. Contains complete documentation structure.

**`src/`, `tests/`, `config/`, `common/`** — Example placeholders. Customize for your project type.

**`mock-data/`** — Sample data files for testing and examples.

## Usage

(README)[/documentation/abstract.md]
