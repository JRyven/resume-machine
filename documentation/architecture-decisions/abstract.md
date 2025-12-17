---
project_name: JSON CV
title: Architecture Decision Records (Index)
description: Index and guidelines for documenting architectural decisions using ADRs.
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [adr, architecture, decisions, documentation]
---

# Architecture Decision Records

This is the **central index** for all Architecture Decision Records (ADRs). ADRs capture important architectural decisions made along with their context and consequences. Whether you're proposing a new technical decision, reviewing past choices, or understanding the evolution of the system architecture, start here.

---

## Executive Summary

Architecture Decision Records (ADRs) document significant architectural and technical decisions, providing historical context, rationale, and consequences. The ADR system helps teams understand why decisions were made, track architectural evolution, and avoid rehashing past discussions. ADRs follow a structured lifecycle (Proposed → Accepted/Rejected → Deprecated/Superseded) and should be created for decisions that significantly impact architecture, are difficult to reverse, or involve meaningful trade-offs.

**Best Practices Checklist:**
- [ ] Create ADRs for significant architectural decisions only
- [ ] Use the standard ADR template for consistency
- [ ] Include context, decision rationale, and consequences
- [ ] Document alternatives considered and why they were rejected
- [ ] Update status as decisions evolve (Deprecated/Superseded)
- [ ] Link ADRs from relevant documentation
- [ ] Review ADRs during onboarding and architectural discussions

---

## Table of Contents

1. [Quick Links](#quick-links)
2. [Getting Started](#getting-started)
3. [Core ADR Topics](#core-adr-topics)
4. [Related Documentation](#related-documentation)

---

## Quick Links

**Essential Resources:**
- [ADR Template](./template.md) - Standard template for creating new ADRs
- [ADR List](#adr-list) - Complete list of all project ADRs

**Most Referenced Docs:**
- [What are ADRs?](#what-are-adrs) - Understanding the purpose and benefits
- [When to Create an ADR](#when-to-create-an-adr) - Decision criteria for ADR creation
- [How to Propose an ADR](#how-to-propose-an-adr) - Step-by-step ADR creation process

---

## Getting Started

### For New Contributors

If you're new to Architecture Decision Records, follow this recommended reading order:

1. **[What are ADRs?](#what-are-adrs)** - Understand the purpose, benefits, and lifecycle of ADRs
2. **[When to Create an ADR](#when-to-create-an-adr)** - Learn decision criteria and appropriate use cases
3. **[How to Propose an ADR](#how-to-propose-an-adr)** - Follow the step-by-step ADR creation process
4. **[ADR Template](./template.md)** - Review the standard ADR structure
5. **[ADR List](#adr-list)** - Explore existing ADRs for examples and context

### Quick Start Checklist

- [ ] Read [What are ADRs?](#what-are-adrs) to understand the concept
- [ ] Review [When to Create an ADR](#when-to-create-an-adr) decision criteria
- [ ] Copy the [ADR Template](./template.md) for new decisions
- [ ] Follow the [ADR Proposal Process](#how-to-propose-an-adr)
- [ ] Link your ADR from relevant documentation
- [ ] Add your ADR to the [ADR List](#adr-list)

---

## What are ADRs?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

**ADRs help:**
- Document the reasoning behind technical choices
- Provide context for future developers
- Track the evolution of the system architecture
- Enable better decision-making through historical reference

### Why Use ADRs?

- **Historical Context:** Understand why decisions were made months or years later
- **Knowledge Sharing:** Onboard new team members with architectural reasoning
- **Decision Tracking:** Maintain a record of significant technical choices
- **Prevent Revisiting:** Avoid rehashing old discussions
- **Accountability:** Clear ownership and rationale for decisions

### ADR Lifecycle

ADRs can have the following statuses:

1. **Proposed:** Initial ADR created, under review
2. **Accepted:** Decision approved and implemented
3. **Deprecated:** Decision still in effect but being phased out
4. **Superseded:** Replaced by a newer ADR (link to successor)
5. **Rejected:** Proposal was not accepted

---

## When to Create an ADR

Create an ADR when making decisions about:
- System architecture patterns (e.g., choosing Clean Architecture)
- Technology stack choices (e.g., selecting a database)
- Major refactoring approaches
- Security implementations
- Performance optimization strategies
- API design patterns
- Data modeling approaches
- Third-party integrations

**Create an ADR for decisions that:**

- ✅ **Significantly impact architecture** (e.g., choosing a database, framework, or design pattern)
- ✅ **Are difficult to reverse** (e.g., selecting a programming language, cloud provider)
- ✅ **Affect multiple components** (e.g., authentication strategy, API design)
- ✅ **Involve trade-offs** (e.g., performance vs. simplicity, cost vs. features)
- ✅ **Require stakeholder agreement** (e.g., major technology shifts)

**Don't create ADRs for:**

- ❌ Trivial or easily reversible decisions
- ❌ Implementation details within a single module
- ❌ Routine bug fixes or refactoring
- ❌ Decisions that don't affect architecture

---

## Core ADR Topics

### Creating ADRs

**[How to Propose an ADR](#how-to-propose-an-adr)**
Step-by-step process for creating, reviewing, and finalizing new ADRs.

**[ADR Template](./template.md)**
Standard template with all required sections for new Architecture Decision Records.

**[Best Practices](#best-practices)**
Guidelines for writing effective, maintainable ADRs.

### Managing ADRs

**[ADR List](#adr-list)**
Complete list of all project ADRs, organized by status (Active, Deprecated, Superseded).

**[ADR Lifecycle](#adr-lifecycle)**
Understanding ADR status transitions and maintaining ADRs over time.

---

## How to Propose an ADR

Follow these steps to create and propose a new ADR:

### Step 1: Copy the Template

```bash
cp template.md [YYYYMMDD]-[feature]-[decision].md
```

**Naming Convention:** `[YYYYMMDD]-[feature]-[decision].md`

**Examples:**
- `20251016-auth-oauth2.md` - Decision to use OAuth 2.0 for authentication
- `20251020-database-postgresql.md` - Selection of PostgreSQL as primary database
- `20251025-state-management-redux.md` - Choosing Redux for state management

### Step 2: Fill in the Template

Complete all sections of the ADR template:

1. **Title:** Clear, descriptive title
2. **Status:** Proposed, Accepted, Deprecated, Superseded, or Rejected
3. **Context:** Explain the situation and forces at play
4. **Decision:** State the decision clearly
5. **Consequences:** Describe positive and negative outcomes
6. **Alternatives Considered:** List and explain rejected options

### Step 3: Review and Discussion

1. **Share with team:** Circulate the ADR for feedback
2. **Discuss:** Address questions and concerns
3. **Revise:** Update based on feedback
4. **Approve:** Get sign-off from stakeholders

### Step 4: Finalize

1. **Update status** to "Accepted" (or "Rejected")
2. **Add to ADR List** in this document
3. **Link from relevant docs** (e.g., Architecture Overview)
4. **Commit to repository**

---

## ADR List

### Active ADRs

| Number | Title | Date | Status | Description |
|--------|-------|------|--------|-------------|
| [001] | [Decision Title] | [Date] | Accepted | [Brief description] |
| [002] | [Decision Title] | [Date] | Accepted | [Brief description] |

### Deprecated/Superseded ADRs

| Number | Title | Date | Status | Superseded By |
|--------|-------|------|--------|---------------|
| [000] | [Old Decision] | [Date] | Superseded | ADR-003 |

---

## Best Practices

### Writing Effective ADRs

- **Be concise:** ADRs should be short (1-2 pages)
- **Be specific:** Clearly state the decision and rationale
- **Include context:** Explain why the decision was needed
- **Document trade-offs:** Acknowledge both pros and cons
- **List alternatives:** Show what else was considered
- **Use plain language:** Avoid jargon when possible

### Maintaining ADRs

- **Update status:** When decisions change, update or create new ADRs
- **Link ADRs:** Reference related ADRs in "Related" sections
- **Archive old ADRs:** Mark as Superseded, don't delete
- **Review periodically:** Revisit ADRs during architecture reviews

---

## Related Documentation

- [README](../../README.md): Project overview and documentation index
- [Development Guide](../dev/dev-abstract.md): Development processes and standards
- [Documentation Guide](../dev/documentation-abstract.md): Documentation guidelines
- [Roadmap](../dev/roadmap-abstract.md): Project roadmap and milestones
