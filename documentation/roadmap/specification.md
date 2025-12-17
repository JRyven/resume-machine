---
project_name: JSON CV
title: Roadmap Specifications
description: Specifications for writing and updating project roadmap documentation.
last_updated: 2025-12-17
cleardoc_version: 2.3.0
keywords: [roadmap, specifications]
---

# Markdown Roadmap Kanban System Specification

## System Overview

This specification defines a dual-lifecycle task management system implemented in markdown outline format, designed for use with AI agents (LLMs) in software development workflows. The system manages **Projects** through a roadmap lifecycle while simultaneously managing **Tasks** within each project through a Kanban-like lifecycle.

### Dual-Lifecycle Architecture

The system operates on two distinct hierarchical levels:

**Level 1: Roadmap Lifecycle (Projects)**
Projects represent complete features, functionalities, or deliverables. They move through a linear roadmap with four stages: In Progress, Backlog, Complete, and Rejected. Projects are represented as H4 headings within H3 lifecycle stage sections.

**Level 2: Kanban Lifecycle (Tasks)**
Within each project, Tasks represent discrete units of work that move through their own three-stage lifecycle: In Progress, Backlog, and Complete. Tasks are represented as H5 headings within H5 lifecycle stage subsections under each project. Tasks contain Actions (minimal-scope work items) represented as markdown checkboxes.

### Work-In-Progress Limits

To maintain focus and prevent context-switching, the system enforces strict WIP limits:
- **Projects**: Maximum 1 project in "In Progress" at any time
- **Tasks**: Maximum 2 tasks in "In Progress" per project at any time

These limits must be enforced manually by the user when moving items between stages.

---

## Structural Hierarchy

### H3: Project Roadmap Stages

The top-level organization uses H3 headings to denote project lifecycle stages. These appear in the following mandatory order:

1. **In Progress** - Contains exactly 0 or 1 project currently under active development
2. **Backlog** - Contains projects planned for future development, ordered by priority
3. **Complete** - Contains finished projects with abbreviated documentation
4. **Rejected** - Contains abandoned projects with rationale preserved

### H4: Project Headings

Each project is represented by an H4 heading with a descriptive name in brackets:

```markdown
#### [Project Name]
```

Immediately following the project heading is a horizontal rule (`---`) followed by a status section, followed by another horizontal rule. The status section contains paragraph-form information crucial for orienting both LLMs and human developers on the current state of the project. This may include code snippets, bulleted lists, ordered lists, and external references (URLs).

```markdown
#### [Project Name]
---
Current status and context information goes here. This can include multiple paragraphs, code examples, and references that help orient developers to the project's current state.
---
```

Following the status section, projects include metadata fields formatted as `key: value` pairs:

```markdown
created: 2025-12-17
dependencies: [markdown anchor links to prerequisite projects]
priority: low|medium|high
```

### H5: Task Lifecycle Stages (Within Projects)

Within each project, tasks are organized into their own lifecycle stages using H5 headings in this mandatory order:

1. **In Progress** - Contains 0-2 tasks currently being worked on
2. **Backlog** - Contains tasks planned for this project, ordered by intended execution sequence
3. **Complete** - Contains finished tasks with abbreviated documentation

Each stage section must include a WIP limit reminder:

```markdown
##### In Progress
⚠️ LIMIT: Maximum 2 tasks in this section
```

### H5: Task Headings

Individual tasks appear as H5 headings within their lifecycle stage sections:

```markdown
##### [Task Name]
```

The task heading is immediately followed by 1-2 sentences of information crucial to guiding the LLM development methodology. Optionally, this may be followed by additional paragraph-form information and/or code examples in fenced code blocks.

Task metadata follows immediately after the task description:

```markdown
assigned-to: [engineer specialization, e.g., "PHP Engineer"]
dependencies: [markdown anchor links to prerequisite tasks]
```

### Markdown Checkbox Actions

Under each task, minimal-scope actions are represented as markdown checkboxes. These are the atomic work units that must be completed:

```markdown
- [ ] [Action Name]: 1-2 sentences of information crucial to guiding the LLM development methodology.
```

Actions may optionally include additional paragraph-form information and/or code examples indented under the checkbox. When checked (`- [x]`), the action is considered complete.

### H6: Notes Sections (Optional)

Projects may include an H6 `##### Notes` section to capture contextual information that doesn't belong in the status section. This appears after all task lifecycle sections.

Tasks may include an H7 `####### Notes` section for task-specific contextual information. This appears after all actions but before the next task heading.

Notes sections should not duplicate information already present in status sections.

---

## Metadata Requirements

### Project Metadata

Every project in In Progress or Backlog status must include the following metadata immediately after its status section:

```markdown
created: 2025-12-17
dependencies: [#anchor-to-project], [#another-project]
priority: low|medium|high
```

**Field Specifications:**
- `created`: Date in ISO 8601 format (2025-12-17) indicating when the project was added to the roadmap
- `dependencies`: Comma-separated list of markdown anchor links to other projects that must be completed before this project can be started. Use `none` if no dependencies exist
- `priority`: One of three values: `low`, `medium`, or `high`

Projects in Complete or Rejected status retain only:
- `created` date
- For Rejected projects: a `why: [explanation]` field describing the rejection rationale

### Task Metadata

Every task in In Progress or Backlog status must include the following metadata:

```markdown
assigned-to: [engineer specialization]
dependencies: [#anchor-to-task], [#another-task]
```

**Field Specifications:**
- `assigned-to`: A description of the required engineer specialization or role (e.g., "Frontend Engineer", "Database Architect", "PHP Engineer")
- `dependencies`: Comma-separated list of markdown anchor links to other tasks that must be completed before this task can be started. Use `none` if no dependencies exist

Tasks in Complete status retain no metadata.

### Markdown Anchor Link Format

Dependencies reference other projects or tasks using markdown anchor links. These are automatically generated from heading text:

- Convert heading text to lowercase
- Replace spaces with hyphens
- Remove special characters except hyphens
- Prepend with `#`

**Example:**
- Heading: `#### [User Authentication System]`
- Anchor: `#user-authentication-system`
- Reference: `dependencies: [#user-authentication-system]`

---

## Content Detail Requirements

### Detail Retention by Status

The level of detail retained varies based on an item's lifecycle status:

**In Progress / Backlog Status:**
- Full descriptive text (1-2 sentence summaries plus optional additional paragraphs)
- All code examples in fenced code blocks
- All metadata fields
- Complete action lists with descriptions
- Optional notes sections

**Complete Status:**
- Brief descriptive text only (1-2 sentences maximum)
- Metadata removed except `created` date for projects
- Code examples removed (refer to version control logs)
- Action descriptions preserved but simplified to single sentence if needed
- Notes sections removed

**Rejected Status (Projects Only):**
- Brief descriptive text explaining what was attempted
- All metadata removed except `created` date
- Single `why: [explanation]` field added to explain rejection rationale
- Code examples removed
- Task/action details removed entirely

### Code Examples and Extended Information

Code examples and extended explanatory information may appear at three levels:

1. **Project Level**: Within the status section between horizontal rules
2. **Task Level**: Immediately following the task heading and 1-2 sentence summary
3. **Action Level**: Indented under the markdown checkbox

All code examples must use fenced code blocks with appropriate language identifiers:

````markdown
```javascript
function example() {
  return true;
}
```
````

Extended information should be formatted as paragraphs or markdown lists (bulleted or ordered) as appropriate for the content.

---

## Movement and Modification Rules

### Project Movement Rules

Projects move through the roadmap lifecycle according to these rules:

**Backlog → In Progress:**
- Only permitted when no other project occupies the In Progress section (WIP limit: 1)
- All dependencies must be in Complete status
- User must manually move the project and all its content
- Project retains all detail and metadata

**In Progress → Complete:**
- Only permitted when all tasks within the project are in Complete status
- User must manually move the project
- Upon moving, strip all code examples, extended paragraphs, and task/action details
- Retain only brief descriptions and the `created` date
- Remove all other metadata
- Remove any notes sections

**In Progress → Rejected:**
- May occur at any time based on user decision
- User must manually move the project
- Upon moving, strip all code examples and task/action details
- Retain only brief description of what was attempted
- Remove all metadata except `created` date
- Add `why: [explanation]` field with rejection rationale

**Backlog → Rejected:**
- May occur at any time based on user decision
- Same stripping rules as In Progress → Rejected

### Task Movement Rules

Tasks move through the Kanban lifecycle according to these rules:

**Backlog → In Progress:**
- Only permitted when fewer than 2 tasks occupy the In Progress section of that project (WIP limit: 2)
- All task dependencies must be in Complete status
- Task automatically moves when the system detects completion of dependencies and available capacity
- Task retains all detail and metadata

**In Progress → Complete:**
- Automatically triggered when all actions under the task are checked (`- [x]`)
- Upon moving, simplify action descriptions to single sentences if needed
- Remove all code examples and extended paragraphs
- Remove all metadata
- Remove any notes sections
- If this completion reduces In Progress tasks below the WIP limit, automatically promote the next Backlog task

**Automatic Task Queue Advancement:**
When a task moves from In Progress to Complete, the system should automatically move the highest-priority task from Backlog to In Progress, provided:
- The WIP limit of 2 tasks has not been reached
- All dependencies for that task are satisfied

### Adding New Items

**New Projects:**
- Always added to Backlog section (unless explicitly starting a new active project and In Progress is empty)
- Must include all required metadata
- Should include status section with initial context
- Tasks should be pre-planned in the project's Backlog section

**New Tasks:**
- Always added to the project's Backlog section
- Must include all required metadata
- Should have actions pre-defined as unchecked markdown checkboxes

**New Actions:**
- Added as unchecked markdown checkboxes under appropriate task
- Must include 1-2 sentence description minimum
- May include optional extended information and code examples

### Modifying Existing Items

**Updating Descriptions:**
- Permitted at any time for items in In Progress or Backlog
- Keep descriptions accurate and reflective of current understanding
- Update code examples as needed to reflect current approach

**Adding/Removing Actions:**
- Permitted for tasks in In Progress or Backlog
- When removing actions, document reason in task notes if significant
- When adding actions, ensure they maintain minimal scope

**Changing Metadata:**
- Priority changes permitted at any time for projects
- Dependency changes should trigger re-evaluation of readiness
- Assigned-to changes permitted for tasks not yet started

**Status Section Updates:**
- Project status sections should be updated regularly to reflect current state
- Include recent changes, blockers, or significant decisions
- May include references to external resources or documentation

---

## Formal Schema for Programmatic Validation

This schema defines the structure in a format suitable for AI agent validation:

### Document Structure Rules

```
DOCUMENT := HEADER + IN_PROGRESS_PROJECTS + BACKLOG_PROJECTS + COMPLETE_PROJECTS + REJECTED_PROJECTS

HEADER := "# " + ANY_TEXT + NEWLINE

IN_PROGRESS_PROJECTS := "### In Progress" + NEWLINE + "⚠️ LIMIT: Only 1 project allowed in this section" + NEWLINE + PROJECT_ACTIVE{0,1}

BACKLOG_PROJECTS := "### Backlog" + NEWLINE + PROJECT_ACTIVE*

COMPLETE_PROJECTS := "### Complete" + NEWLINE + PROJECT_COMPLETE*

REJECTED_PROJECTS := "### Rejected" + NEWLINE + PROJECT_REJECTED*
```

### Project Structure Rules

```
PROJECT_ACTIVE := PROJECT_HEADING + STATUS_SECTION + PROJECT_METADATA_ACTIVE + TASK_SECTIONS + NOTES_SECTION_PROJECT?

PROJECT_COMPLETE := PROJECT_HEADING + BRIEF_DESCRIPTION + PROJECT_METADATA_COMPLETE + TASK_COMPLETE_LIST?

PROJECT_REJECTED := PROJECT_HEADING + BRIEF_DESCRIPTION + PROJECT_METADATA_REJECTED

PROJECT_HEADING := "#### [" + PROJECT_NAME + "]" + NEWLINE

STATUS_SECTION := "---" + NEWLINE + PARAGRAPH_CONTENT + "---" + NEWLINE

PROJECT_METADATA_ACTIVE := "created: " + ISO_DATE + NEWLINE + "dependencies: " + DEPENDENCY_LIST + NEWLINE + "priority: " + PRIORITY_VALUE + NEWLINE

PROJECT_METADATA_COMPLETE := "created: " + ISO_DATE + NEWLINE

PROJECT_METADATA_REJECTED := "created: " + ISO_DATE + NEWLINE + "why: " + EXPLANATION_TEXT + NEWLINE

NOTES_SECTION_PROJECT := "##### Notes" + NEWLINE + PARAGRAPH_CONTENT
```

### Task Structure Rules

```
TASK_SECTIONS := IN_PROGRESS_TASKS + BACKLOG_TASKS + COMPLETE_TASKS

IN_PROGRESS_TASKS := "##### In Progress" + NEWLINE + "⚠️ LIMIT: Maximum 2 tasks in this section" + NEWLINE + TASK_ACTIVE{0,2}

BACKLOG_TASKS := "##### Backlog" + NEWLINE + TASK_ACTIVE*

COMPLETE_TASKS := "##### Complete" + NEWLINE + TASK_COMPLETE*

TASK_ACTIVE := TASK_HEADING + TASK_DESCRIPTION + TASK_METADATA_ACTIVE + ACTION_LIST + NOTES_SECTION_TASK?

TASK_COMPLETE := TASK_HEADING + BRIEF_DESCRIPTION + ACTION_LIST_SIMPLE

TASK_HEADING := "##### [" + TASK_NAME + "]" + NEWLINE

TASK_DESCRIPTION := SHORT_DESCRIPTION + (EXTENDED_PARAGRAPH | CODE_BLOCK)*

TASK_METADATA_ACTIVE := "assigned-to: " + ROLE_DESCRIPTION + NEWLINE + "dependencies: " + DEPENDENCY_LIST + NEWLINE

NOTES_SECTION_TASK := "####### Notes" + NEWLINE + PARAGRAPH_CONTENT
```

### Action Structure Rules

```
ACTION_LIST := ACTION_ITEM+

ACTION_LIST_SIMPLE := ACTION_ITEM_SIMPLE+

ACTION_ITEM := CHECKBOX + " [" + ACTION_NAME + "]: " + SHORT_DESCRIPTION + (EXTENDED_PARAGRAPH | CODE_BLOCK)* + NEWLINE

ACTION_ITEM_SIMPLE := CHECKBOX + " [" + ACTION_NAME + "]: " + SHORT_DESCRIPTION + NEWLINE

CHECKBOX := "- [ ]" | "- [x]"
```

### Data Type Rules

```
ISO_DATE := YYYY + "-" + MM + "-" + DD
  WHERE YYYY = 4 digits, MM = 01-12, DD = 01-31

DEPENDENCY_LIST := ("none" | ANCHOR_LINK + (", " + ANCHOR_LINK)*)

ANCHOR_LINK := "[#" + ANCHOR_TEXT + "]"
  WHERE ANCHOR_TEXT = lowercase heading text with spaces → hyphens, special chars removed

PRIORITY_VALUE := "low" | "medium" | "high"

SHORT_DESCRIPTION := 1-2 sentences, length ≤ 300 chars

BRIEF_DESCRIPTION := 1-2 sentences, length ≤ 200 chars

EXTENDED_PARAGRAPH := One or more paragraphs with optional lists

CODE_BLOCK := "```" + LANGUAGE_ID + NEWLINE + CODE_CONTENT + "```" + NEWLINE

PARAGRAPH_CONTENT := (TEXT | LIST | CODE_BLOCK)+

PROJECT_NAME := Text without brackets, length ≤ 100 chars

TASK_NAME := Text without brackets, length ≤ 100 chars

ACTION_NAME := Text without brackets, length ≤ 80 chars

ROLE_DESCRIPTION := Text describing engineer specialization, length ≤ 50 chars

EXPLANATION_TEXT := Text explaining rationale, length ≤ 500 chars
```

### Validation Rules

1. **WIP Limit Enforcement**: Parser must validate that "In Progress" project section contains ≤ 1 project
2. **Task WIP Limit Enforcement**: Parser must validate that each project's "In Progress" task section contains ≤ 2 tasks
3. **Date Format Validation**: All dates must match ISO 8601 format (2025-12-17)
4. **Priority Validation**: Priority field must be exactly one of: low, medium, high
5. **Dependency Resolution**: All anchor links in dependencies must resolve to existing headings in the document
6. **Section Order Enforcement**: Project sections must appear in order: In Progress, Backlog, Complete, Rejected
7. **Task Section Order Enforcement**: Task sections must appear in order: In Progress, Backlog, Complete
8. **Metadata Completeness**: All active projects/tasks must have all required metadata fields
9. **Checkbox Format**: All action items must use valid markdown checkbox syntax (- [ ] or - [x])
10. **Heading Level Validation**: Validate correct heading hierarchy (H3→H4→H5→H6→H7)

---

## Example: Before and After Completion

### Before Completion (In Progress)

```markdown
### In Progress
⚠️ LIMIT: Only 1 project allowed in this section

#### [User Authentication System]
'''
Building a secure JWT-based authentication system with role-based access control. Currently implementing the token generation and validation middleware. Using bcrypt for password hashing and storing refresh tokens in Redis for quick invalidation.

Reference: https://jwt.io/introduction
'''
created: 2025-10-15
dependencies: [#database-schema-setup]
priority: high

##### In Progress
⚠️ LIMIT: Maximum 2 tasks in this section

##### [Implement JWT Token Generation]
Create middleware to generate access and refresh tokens upon successful login. Access tokens expire in 15 minutes, refresh tokens in 7 days.

```javascript
function generateTokens(userId, roles) {
  const accessToken = jwt.sign(
    { userId, roles },
    process.env.JWT_SECRET,
    { expiresIn: '15m' }
  );
  return { accessToken, refreshToken };
}
```

assigned-to: Backend Engineer
dependencies: none

- [ ] [Create token generation utility]: Implement function to create JWT access and refresh tokens with appropriate expiration times and payload structure.
    ```javascript
    const jwt = require('jsonwebtoken');
    const crypto = require('crypto');
    ```
- [ ] [Store refresh token in Redis]: Save refresh token to Redis with user ID as key and 7-day expiration.
    Use the node-redis client and set TTL to match token expiration.
- [x] [Add token signing secret to environment]: Configure JWT_SECRET in .env file and validate it exists on application startup.

####### Notes
Consider rotating the JWT_SECRET periodically. May need to implement a key versioning system in the future.

##### [Create Authentication Middleware]
Build Express middleware to validate JWT tokens on protected routes.

assigned-to: Backend Engineer
dependencies: [#implement-jwt-token-generation]

- [ ] [Extract token from Authorization header]: Parse the Bearer token from incoming requests and handle missing or malformed headers gracefully.
- [ ] [Verify token signature]: Use jwt.verify() to validate the token signature and expiration.
- [ ] [Attach user data to request object]: After successful verification, attach decoded user ID and roles to req.user for downstream handlers.

##### Backlog

##### [Implement Password Reset Flow]
Allow users to request password reset via email with time-limited token.

assigned-to: Backend Engineer
dependencies: [#create-authentication-middleware]

- [ ] [Generate reset token]: Create cryptographically secure random token and store with expiration in Redis.
- [ ] [Send reset email]: Integrate with email service to send reset link to user.
- [ ] [Validate and process reset]: Verify token validity and update user password in database.

##### Complete
```

### After Completion (Moved to Complete)

```markdown
### Complete

#### [User Authentication System]
JWT-based authentication system with role-based access control. Implemented token generation, validation middleware, and password reset flow.

created: 2025-10-15

##### [Implement JWT Token Generation]
Created middleware to generate access and refresh tokens.

- [x] [Create token generation utility]
- [x] [Store refresh token in Redis]
- [x] [Add token signing secret to environment]

##### [Create Authentication Middleware]
Built Express middleware to validate JWT tokens.

- [x] [Extract token from Authorization header]
- [x] [Verify token signature]
- [x] [Attach user data to request object]

##### [Implement Password Reset Flow]
Implemented password reset via email with time-limited tokens.

- [x] [Generate reset token]
- [x] [Send reset email]
- [x] [Validate and process reset]
```

### Example: Rejected Project

```markdown
### Rejected

#### [Real-time Collaborative Editing]
Attempted to implement operational transformation for real-time document collaboration using custom WebSocket server.

created: 2025-09-20
why: After prototyping, discovered that operational transformation complexity exceeded team expertise. Decided to use established library (Yjs) instead, which will be tracked as a new project.
```

---

## Complete Template

```markdown
# Project Roadmap

### In Progress
⚠️ LIMIT: Only 1 project allowed in this section

#### [Project Name]
'''
Status information goes here. Current state, recent changes, blockers, decisions. Can include code snippets, lists, and external references.

```language
code examples
```

Additional context paragraphs as needed.
'''
created: 2025-12-17
dependencies: [#other-project], [#another-project] or none
priority: low|medium|high

##### In Progress
⚠️ LIMIT: Maximum 2 tasks in this section

##### [Task Name]
Brief 1-2 sentence description of the task.

Optional additional paragraphs explaining approach or context.

```language
optional code example
```

assigned-to: Engineer Specialization
dependencies: [#other-task] or none

- [ ] [Action Name]: Brief description of this action.
    Optional extended information.
    ```language
    optional code example
    ```
- [ ] [Action Name]: Brief description of this action.

####### Notes
Optional task-specific notes that don't belong in the main description.

##### Backlog

##### [Task Name]
Brief 1-2 sentence description.

assigned-to: Engineer Specialization
dependencies: [prerequisite-task] or none

- [ ] [Action Name]: Brief description.
- [ ] [Action Name]: Brief description.

##### Complete

##### [Task Name]
Brief description.

- [x] [Action Name]
- [x] [Action Name]

##### Notes
Optional project-level notes.

### Backlog

#### [Project Name]
'''
Status and context information.
'''
created: 2025-12-17
dependencies: [prerequisite-project] or none
priority: low|medium|high

##### In Progress
⚠️ LIMIT: Maximum 2 tasks in this section

##### Backlog

##### [Task Name]
Description.

assigned-to: Engineer Specialization
dependencies: none

- [ ] [Action Name]: Description.

##### Complete

### Complete

#### [Project Name]
Brief summary of what was completed.

created: 2025-12-17

##### [Task Name]
Brief summary.

- [x] [Action Name]
- [x] [Action Name]

### Rejected

#### [Project Name]
Brief description of what was attempted.

created: 2025-12-17
why: Explanation of why this project was abandoned and what decision was made instead.
```

---

## Best Practices for AI Agents

When working with this system, AI agents should:

1. **Always validate structure** against the formal schema before making modifications
2. **Check WIP limits** before suggesting moving items to In Progress
3. **Verify dependencies** are satisfied before promoting tasks or projects
4. **Preserve detail** for active work while stripping completed/rejected items
5. **Use anchor links correctly** for all dependency references
6. **Maintain date formats** in ISO 8601 (2025-12-17)
7. **Keep action scope minimal** - if an action seems too large, break it into multiple actions
8. **Update status sections regularly** to reflect current understanding
9. **Check boxes as work completes** and trigger automatic task promotions
10. **Document rejection rationale clearly** in the why field

When asked to modify the roadmap, AI agents should:
- Confirm the change doesn't violate WIP limits
- Verify all dependencies are satisfied
- Maintain proper heading hierarchy
- Preserve or strip detail based on destination status
- Update metadata appropriately
- Validate the entire document structure after changes
