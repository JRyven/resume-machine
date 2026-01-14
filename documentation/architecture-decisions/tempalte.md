---
project_name: [PROJECT_NAME]
title: [SHORT_TITLE]
description: [SHORT_DESCRIPTION]
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [adr, architecture, decisions, documentation]
---

# ADR [Number]: [Short Title]

**Date:** [YYYY-MM-DD]
**Status:** [Proposed | Accepted | Deprecated | Superseded]
**Deciders:** [List of people involved in the decision]
**Related ADRs:** [Links to related ADRs, if any]

## Context

Describe the context and problem statement that led to this decision. What is the issue we're trying to solve? What are the constraints? What are the requirements?

Include:
- Background information
- The problem or need driving the decision
- Any constraints (technical, business, regulatory)
- Key stakeholders or affected parties

## Decision

State the decision clearly and concisely. What did we decide to do?

Be specific about:
- The chosen solution or approach
- Key components of the implementation
- Any important configurations or patterns
- Why this particular approach was selected

## Alternatives Considered

List and briefly describe the alternatives that were considered. For each alternative, explain why it was not chosen.

### Alternative 1: [Name]
- **Description:** Brief explanation
- **Pros:** Benefits of this approach
- **Cons:** Drawbacks or limitations
- **Reason for rejection:** Why we didn't choose this

### Alternative 2: [Name]
- **Description:** Brief explanation
- **Pros:** Benefits of this approach
- **Cons:** Drawbacks or limitations
- **Reason for rejection:** Why we didn't choose this

## Consequences

### Positive
- What benefits does this decision provide?
- What problems does it solve?
- What opportunities does it create?

### Negative
- What are the downsides or trade-offs?
- What technical debt might this create?
- What complexity is added?

### Neutral
- What other impacts will this have?
- What remains unchanged?
- What new concerns or considerations arise?

## Implementation Notes

Technical details about implementing this decision:
- Key files or modules affected
- Dependencies to add or remove
- Configuration changes needed
- Migration steps if applicable
- Testing considerations

## Validation

How will we know if this decision was successful?
- Success criteria
- Metrics to monitor
- Timeline for evaluation
- Conditions that might trigger a reassessment

## References

- [Link to relevant documentation]
- [Link to research or articles that informed the decision]
- [Link to proof-of-concept code or experiments]
- [Related issues or discussions]

---

## Example ADR

For a concrete example, here's a simplified real-world ADR:

---

# ADR 001: Use Clean Architecture Pattern

**Date:** 2025-10-15
**Status:** Accepted
**Deciders:** Development Team

## Context

We need an architectural pattern that provides clear separation of concerns, makes the codebase testable, and allows for future flexibility in changing frameworks or technologies.

## Decision

Adopt Clean Architecture with three main layers:
- **Domain Layer:** Pure business logic and entities
- **Data Layer:** Data access and external service integration
- **Presentation Layer:** UI and user interaction handling

## Alternatives Considered

### Layered Architecture
- **Pros:** Simple, well-understood
- **Cons:** Can lead to tight coupling between layers
- **Reason for rejection:** Doesn't enforce dependency inversion

### Microservices
- **Pros:** Ultimate flexibility and scalability
- **Cons:** Overly complex for current project size
- **Reason for rejection:** Adds unnecessary operational overhead

## Consequences

### Positive
- Clear boundaries between business logic and technical details
- Highly testable code
- Easy to swap out frameworks or data sources

### Negative
- More boilerplate code initially
- Steeper learning curve for developers new to the pattern

## Implementation Notes

- Use repository interfaces in domain layer
- Implement dependency injection
- Write use cases as single-purpose classes
- Keep domain layer framework-independent

## Validation

Success metrics:
- Unit test coverage >85%
- Ability to run domain tests without any framework dependencies
- New features can be added without modifying existing layers

---
