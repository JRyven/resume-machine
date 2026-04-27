---
project_name: [PROJECT_NAME]
title: ADR Specification
description: Rules for creating Architecture Decision Records documenting major technical decisions.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [adr, architecture, decision, record, specification]
---

# ADR Specification

**Path:** Documentation > Writing Documentation > ADR Specification

An Architecture Decision Record (ADR) documents a significant architectural decision made during project development, including the rationale and consequences.

## Purpose

ADRs create a decision log that:

- Records why architectural choices were made
- Preserves context and alternatives considered
- Helps future developers understand design trade-offs
- Serves as learning documentation for the team

## Status Values

Each ADR must have one of these status values:

- **Proposed** - Decision under consideration, not yet approved
- **Accepted** - Decision approved and currently in use
- **Deprecated** - Decision was used but is no longer recommended
- **Superseded** - Decision replaced by a newer decision (link to the new ADR)

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: [ADR_NUMBER] - [DECISION_TITLE]
description: [BRIEF_DECISION_SUMMARY]
status: [Proposed|Accepted|Deprecated|Superseded]
decision_date: [YYYY-MM-DD]
authors: [AUTHOR_NAME]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [adr, architecture, [DOMAIN], [KEYWORD]]
---
```

- `title`: Format as "ADR-XXX - Decision Title"
- `status`: One of the four status values
- `decision_date`: Date decision was made
- `authors`: Decision maker(s)

### Breadcrumb Navigation

```markdown
**Path:** Documentation > Architecture Decisions > [DECISION_TITLE]
```

### Context

Explain what problem this decision addresses. Include:

- The architectural issue or problem statement
- Constraints and requirements driving the decision
- Business context if relevant
- Deadline or urgency if applicable

### Options Considered

List alternatives evaluated. For each option include:

- Brief description of the approach
- Key trade-offs (advantages and disadvantages)
- Resource requirements if significant

Minimum 2 options; list the chosen option last.

### Decision

Statement of the decision made, phrased as a resolved statement:

> We will use [TECHNOLOGY/PATTERN/APPROACH] to [ACHIEVE_THIS_OUTCOME].

### Consequences

Explain what will happen as a result of this decision:

**Positive Consequences:**

- Benefits, improvements, or capabilities gained

**Negative Consequences:**

- Trade-offs, added complexity, or resource impacts

**Neutral Consequences:**

- Ongoing maintenance requirements or dependencies

## Optional Sections

### Related Decisions

Link to related ADRs that provide context or contrast:

- [ADR-001 - Previous Decision](./adr-001.md)
- [ADR-003 - Complementary Decision](./adr-003.md)

### Implementation Notes

Technical details on how to implement or migrate to this decision.

## Example

```markdown
---
project_name: [PROJECT_NAME]
title: ADR-005 - Use PostgreSQL for Primary Data Store
description: Decision to use PostgreSQL instead of MongoDB for relational data.
status: Accepted
decision_date: 2025-08-15
authors: [ARCHITECTURE_TEAM]
last_updated: 2025-12-20
cleardoc_version: 2.3.0
keywords: [adr, architecture, database, postgresql]
---

# ADR-005 - Use PostgreSQL for Primary Data Store

**Path:** Documentation > Architecture Decisions > Use PostgreSQL for Primary Data Store

## Context

Application requires storing relational data with complex queries. Team needed to decide between PostgreSQL (relational) and MongoDB (document-based).

Requirements:

- Complex joins across multiple entities
- ACID transaction guarantees required
- Read-heavy workload with complex queries
- Team has PostgreSQL expertise

## Options Considered

### Option 1: MongoDB

Document-oriented database with flexible schema. Advantages: fast writes, horizontal scaling. Disadvantages: weak transaction support, complex joins require application-level logic.

### Option 2: PostgreSQL

Relational database with strong ACID guarantees. Advantages: native joins, proven scalability, strong consistency. Disadvantages: vertical scaling focus, requires schema design upfront.

### Option 3: DynamoDB

AWS managed service with pay-per-use pricing. Advantages: fully managed, auto-scaling. Disadvantages: vendor lock-in, limited query flexibility, expensive at scale.

## Decision

We will use **PostgreSQL** as the primary data store for relational data because it provides ACID guarantees and native join support required by our query patterns.

## Consequences

**Positive:**

- Complex queries can be expressed directly in SQL
- ACID transactions ensure data consistency
- Team expertise reduces ramp-up time

**Negative:**

- Schema changes require migration planning
- Vertical scaling limits for very large datasets
- Connection pooling complexity

**Neutral:**

- Requires DBA skills for optimization
- Ongoing backup and recovery procedures
- Monitoring and alerting setup needed

## Related Decisions

- [ADR-003 - Microservices Architecture](./adr-003.md) - Data store decision supports this pattern
- [ADR-008 - Read Replicas for Reporting](./adr-008.md) - Scaling strategy for read-heavy workloads
```

## Size Guidelines

- Total: 300-600 words
- YAML: ~50 words
- Breadcrumb: 5 words
- Context: 80-100 words
- Options: 100-150 words (30-50 per option)
- Decision: 20-30 words
- Consequences: 80-120 words
