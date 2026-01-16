---
project_name: [PROJECT_NAME]
title: Roadmap Guide (Index)
description: Index and overview of project planning documentation covering initial development and long-term maintenance phases.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
phase: abstract
development_goals_location: none
keywords: [roadmap, planning, development goals, phases, index]
---

# Roadmap Guide

This is the **central index** for all project planning and roadmap documentation. Whether you're planning initial development, managing maintenance phases, or making strategic decisions, start here to find the right roadmap guidance.

---

## Executive Summary

The Roadmap Guide provides comprehensive planning documentation for project lifecycle management, from initial development through long-term maintenance. Key focus areas include phased development approaches, Development Goals tracking, and strategic planning for sustainable growth. Use this guide to determine which roadmap applies to your current project phase and access relevant planning resources.

**Best Practices Checklist:**

- [ ] Review appropriate roadmap based on current project phase
- [ ] Align team efforts with roadmap priorities and development goals
- [ ] Update Development Goals statuses as work progresses
- [ ] Create ADRs for significant roadmap changes
- [ ] Regularly review and adjust roadmap based on project realities
- [ ] Document phase transitions and lessons learned

---

## Definitions

Understanding these key terms is essential for working with the roadmap system:

**Project:** A complete feature, functionality, or deliverable represented as an H4 heading in the Development Goals section. Projects move through the Roadmap Lifecycle (In Progress → Backlog → Complete → Rejected).

**Task:** A discrete unit of work within a project, represented as an H5 heading. Tasks move through their own Kanban Lifecycle (In Progress → Backlog → Complete) within each project.

**Action:** A minimal-scope work item represented as a markdown checkbox (`- [ ]` or `- [x]`) under a task. Actions are the atomic units of work that must be completed.

**Roadmap Lifecycle:** The progression path for projects through four stages: In Progress, Backlog, Complete, and Rejected. This lifecycle tracks overall project status across the product roadmap.

**Kanban Lifecycle:** The progression path for tasks within a project through three stages: In Progress, Backlog, and Complete. This lifecycle enables granular tracking of work within each project.

**WIP Limits (Work-In-Progress Limits):** Constraints that prevent overload and maintain focus:

- **Project WIP Limit:** Maximum 1 project in "In Progress" status at any time

**Development Goals:** The collective term for all projects being tracked through the Development Goals tracking system in the Unified Development Roadmap, covering all project phases from inception through long-term maintenance and growth.

**MVP (Minimum Viable Product):** The initial production-ready version of the application containing core functionality sufficient for launch. Achievement of MVP marks the transition from Initial Development to Maintenance phase.

For complete technical specifications of the Development Goals tracking system, see the [Roadmap Specification](./specification.md).

---

## Table of Contents

1. [Quick Links](#quick-links)
2. [Getting Started](#getting-started)
3. [Core Planning Topics](#core-planning-topics)
4. [How to Use This Roadmap](#how-to-use-this-roadmap)
5. [Risk Management](#risk-management)
6. [Related Documentation](#related-documentation)

---

## Getting Started

### For New Projects

If you're planning a new project, follow this recommended reading order:

1. **[Unified Development Roadmap](./roadmap.md)** - Complete planning framework for all project development phases
2. **[Roadmap Specification](./specification.md)** - Technical reference for Development Goals tracking structure and rules

### For Established Projects

If you're managing an ongoing project, follow this maintenance-focused approach:

1. **[Unified Development Roadmap](./roadmap.md)** - Long-term planning for feature enhancement and sustainability
2. **[Roadmap Specification](./specification.md)** - Technical reference for Development Goals tracking structure and rules

### Quick Start Checklist

- [ ] Read the [Roadmap Specification](./specification.md) to understand the Development Goals tracking system
- [ ] Identify current development goals and upcoming priorities
- [ ] Align objectives with roadmap goals
- [ ] Document any significant deviations or changes

---

## Core Planning Topics

### Development Goals Tracking System

The Development Goals tracking system is a dual-lifecycle markdown-based task management approach designed for both human and AI agent collaboration. Projects progress through a roadmap lifecycle (In Progress → Backlog → Complete → Rejected).

**Key Features:**

- **Dual-lifecycle architecture** for managing both strategic projects and tactical tasks
- **WIP limits** to maintain focus
- **Structured metadata** for dependencies, priorities, and assignments
- **Automatic task progression** as actions are completed
- **Programmatic validation** schema for AI agent integration

**Where Development Goals Live:**

- **All Phases:** All projects across the entire development lifecycle are tracked in [roadmap.md](./roadmap.md)
- **Specification:** Complete technical documentation in [specification.md](./specification.md)

**When to Update Development Goals:**

- When work is completed (tasks finish, projects complete)
- When new decisions are made (new projects identified, priorities change)
- When dependencies change or blockers are resolved
- When projects are abandoned (move to Rejected with rationale)

Both human developers and AI agents edit these documents directly, with all changes tracked through version control.

### All Development Phases

**[Unified Development Roadmap](./roadmap.md)**
Comprehensive planning framework covering all project development phases:

- **Initial Development:** Project setup, foundation, core feature development, testing, deployment
- **Post-Launch:** Stabilization, monitoring, feature enhancements, and iterative improvements
- **Maintenance & Growth:** Performance optimization, technical debt management, user-driven evolution

All projects across the entire development lifecycle are tracked in the Development Goals section of this unified document. The roadmap adapts to your current project phase while maintaining a consistent tracking system.

### Decision Documentation

**[Architecture Decision Records](../../architecture-decisions/README.md)**
Structured documentation of significant planning and architectural decisions:

- ADR templates and guidelines
- Decision rationale and alternatives considered
- Implementation tracking and outcomes
- Historical decision context for future reference

---

## How to Use This Roadmap

This section provides comprehensive guidance for both human developers and AI agents working with the roadmap documentation system.

### As Project Manager

1. **Track progress**
   - Monitor project and task completion in Development Goals sections
   - Review WIP limits to ensure focus is maintained
   - Check dependency chains to identify potential blockers

2. **Monitor risks** and implement mitigation strategies
   - Review the [Risk Management](#risk-management) section regularly
   - Create projects in Development Goals backlog for critical risks requiring mitigation work
   - Document risk decisions in ADRs when appropriate

3. **Adjust scope** based on feedback and constraints
   - Move projects to Rejected with clear rationale when priorities change
   - Update project priorities and dependencies as understanding evolves
   - Create ADRs for significant scope changes

### As Developer

1. **Focus on sprint goals** and acceptance criteria
   - Work on tasks in the "In Progress" sections
   - Check off actions as they are completed
   - Update task notes with implementation details or challenges

2. **Maintain quality standards** throughout development
   - Follow the development methodologies described in task descriptions
   - Include code examples and detailed guidance in tasks when beneficial
   - Reference the [Roadmap Specification](./specification.md) for structure rules

3. **Provide feedback and new ideas** and provide constructive feedback
   - Suggest new projects or tasks based on technical insights
   - Document learnings in task or project notes sections

4. **Document decisions** and technical approaches
   - Create ADRs for significant architectural decisions
   - Update project status sections with current state and context
   - Preserve rationale when moving projects to Rejected

### As any role

1. **Validate structure** before making modifications
   - Always validate against the formal schema in [specification.md](./specification.md)
   - Check WIP limits before suggesting moves to In Progress
   - Verify dependencies are satisfied before promoting tasks or projects

2. **Preserve detail appropriately** based on status
   - Keep full detail (code examples, extended descriptions) for In Progress and Backlog items
   - Strip code examples and lengthy details when moving to Complete
   - Retain only brief descriptions and "why" rationale for Rejected items

3. **Maintain consistency** across documents
   - Use terminology defined in the [Definitions](#definitions) section
   - Follow metadata formats (YYYY-MM-DD dates, anchor link dependencies)
   - Keep action scope minimal - break large actions into multiple items

4. **Update status sections** to reflect current understanding
   - Include recent changes, blockers, or significant decisions in project status sections
   - Add references to external resources or documentation when relevant
   - Document implementation learnings in notes sections

### Updating the Roadmap

**Update Frequency:**

- **As needed:** When work completes or new decisions are made (no fixed cadence)
- **Before updates:** Review relevant sections of [specification.md](./specification.md) to ensure compliance
- **After updates:** Commit changes to version control with descriptive commit messages

**Who Updates:**

- Both human developers and AI agents edit these documents
- All changes are tracked through version control
- No formal approval process for single-person projects (adapt as team grows)

**What to Update:**

_When completing work:_

- Check off completed actions (`- [ ]` → `- [x]`)
- Move completed tasks from In Progress to Complete (strip detail per spec)
- Move completed projects from In Progress to Complete (strip detail per spec)
- Promote next backlog task automatically when In Progress drops below WIP limit

_When making new decisions:_

- Add new projects to appropriate backlog (Initial or Maintenance)
- Add new tasks to project backlogs with full metadata
- Update priorities or dependencies based on new information
- Move projects to Rejected with clear "why" rationale

_When updating status:_

- Update project status sections with current context
- Add notes to projects or tasks to capture decisions or learnings
- Update Current Project Status section in roadmap-abstract.md
- Update last_modified date in document frontmatter

**Validation Checklist:**

- [ ] WIP limits respected (1 project)
- [ ] All dependencies use correct markdown anchor link format
- [ ] All dates in YYYY-MM-DD format
- [ ] All required metadata present for active projects and tasks
- [ ] Heading hierarchy correct (H3→H4→H5 for project sections)
- [ ] Detail stripped appropriately for items moved to Complete/Rejected
- [ ] Changes committed to version control

---

## Risk Management

Effective risk management is critical throughout all phases of project development and maintenance. Risks should be identified early, monitored continuously, and mitigated proactively. Critical risks may warrant dedicated projects in the Development Goals backlog to ensure proper attention and resources.

### Technical Risks

**Initial Development Phase:**

- **Scope Creep:** Strict prioritization and MVP focus
- **Technology Changes:** Early proof-of-concepts and architecture spikes
- **Performance Issues:** Regular performance testing and optimization
- **Security Vulnerabilities:** Security reviews and automated scanning

**Maintenance Phase:**

- **Dependency Vulnerabilities:** Regular security updates and dependency scanning
- **Performance Degradation:** Continuous monitoring and proactive optimization
- **Technical Debt Accumulation:** Dedicated refactoring time in each sprint
- **Platform Compatibility:** Regular testing across supported platforms

### Project Risks

**Initial Development Phase:**

- **Timeline Delays:** Agile methodology with regular reassessment
- **Resource Constraints:** Cross-training and knowledge sharing
- **Stakeholder Expectations:** Regular demos and transparent communication
- **Market Changes:** Competitive analysis and flexibility in requirements

**Maintenance Phase:**

- **User Retention:** Focus on user experience and feature enhancements
- **Competitive Pressure:** Market monitoring and differentiation strategies
- **Resource Constraints:** Efficient resource allocation and prioritization
- **Regulatory Changes:** Compliance monitoring and adaptation planning

### Operational Risks

**Maintenance Phase (Primary Concern):**

- **Incident Management:** 24/7 monitoring and rapid response capabilities
- **Data Loss:** Robust backup and disaster recovery procedures
- **Team Knowledge:** Documentation and knowledge sharing practices
- **Vendor Dependencies:** Multiple vendor options and contingency planning

### Mitigation Strategies

**Proactive Management:**

- **Regular Risk Reviews:** Assess risks during planning sessions and retrospectives
- **Contingency Planning:** Document alternative approaches for critical paths
- **Early Warning Systems:** Monitor KPIs and trends to detect issues before they escalate
- **Stakeholder Communication:** Maintain transparency with regular updates and feedback loops

**Risk-Driven Project Planning:**

- Critical risks may be addressed through dedicated projects in the Development Goals backlog
- When a risk requires significant mitigation effort, create a project with appropriate priority
- Track risk mitigation work using the same Development Goals system as feature development
- Document risk-related decisions in ADRs for future reference

**Phase-Specific Focus:**

- Initial Development: Focus on technical risks and timeline management
- Maintenance: Shift focus to operational risks and user retention
- Both Phases: Maintain awareness of resource constraints and stakeholder expectations
