---
project_name: JSON CV
title: Code Style Guide
description: Code formatting, naming conventions, and best practices for consistent code quality.
last_updated: 2025-12-17
clear_doc_version: 2.1.0
keywords: [development, code-style, standards, formatting, conventions]
---

# Code Style Guide

This guide defines the code formatting standards, naming conventions, and best practices for mailToMD. Consistent code style improves readability, reduces errors, and facilitates collaboration.

---

## Table of Contents

1. [Overview](#overview)
2. [General Principles](#general-principles)
3. [Formatting Standards](#formatting-standards)
4. [Naming Conventions](#naming-conventions)
5. [Code Organization](#code-organization)
6. [Comments and Documentation](#comments-and-documentation)
7. [Language-Specific Guidelines](#language-specific-guidelines)
8. [Linting and Formatting Tools](#linting-and-formatting-tools)
9. [Code Review Standards](#code-review-standards)
10. [Related Documentation](#related-documentation)

---

## Overview

**Philosophy:** Write code for humans first, computers second. Code should be self-documenting, consistent, and maintainable.

**Key Principles:**
- **Consistency:** Follow established patterns throughout the codebase
- **Readability:** Prioritize clarity over cleverness
- **Simplicity:** Prefer simple, straightforward solutions
- **Maintainability:** Write code that others can easily understand and modify

---

## General Principles

### SOLID Principles

Follow SOLID principles for object-oriented design:

- **S - Single Responsibility:** Each class/module should have one reason to change
- **O - Open/Closed:** Open for extension, closed for modification
- **L - Liskov Substitution:** Subtypes must be substitutable for their base types
- **I - Interface Segregation:** Many specific interfaces are better than one general interface
- **D - Dependency Inversion:** Depend on abstractions, not concretions

### DRY (Don't Repeat Yourself)

- Extract repeated code into reusable functions or classes
- Use configuration files for repeated values
- Create utility functions for common operations

### KISS (Keep It Simple, Stupid)

- Prefer simple solutions over complex ones
- Break complex problems into smaller, manageable pieces
- Avoid premature optimization

### YAGNI (You Aren't Gonna Need It)

- Implement features only when needed
- Avoid speculative generality
- Focus on current requirements

---

## Formatting Standards

### Indentation

- **Spaces vs. Tabs:** [Choose: Spaces (2 or 4) or Tabs]
- **Indentation Size:** [e.g., 2 spaces, 4 spaces]
- **Consistency:** Use the same indentation throughout the project

### Line Length

- **Maximum Line Length:** [e.g., 80 or 120 characters]
- **Rationale:** Improves readability and supports side-by-side diffs
- **Exceptions:** URLs, import statements may exceed the limit

### Whitespace

- **Trailing Whitespace:** Remove all trailing whitespace
- **Blank Lines:** Use blank lines to separate logical sections
- **Spacing Around Operators:** Add spaces around binary operators

**Example:**
```javascript
// Good
const result = a + b * c;

// Bad
const result=a+b*c;
```

### Braces and Brackets

**Brace Style:** [Choose: K&R, Allman, Stroustrup]

**K&R Style (Recommended):**
```javascript
if (condition) {
  // code
} else {
  // code
}
```

**Single-Line Statements:**
```javascript
// Good - Use braces even for single-line statements
if (condition) {
  doSomething();
}

// Bad - Avoid omitting braces
if (condition)
  doSomething();
```

---

## Naming Conventions

### General Rules

- **Descriptive Names:** Use clear, descriptive names that reveal intent
- **Avoid Abbreviations:** Write full words unless abbreviation is well-known
- **Searchable Names:** Use names that are easy to search for

### Variables

**Convention:** [camelCase, snake_case, etc.]

**Examples:**
```javascript
// Good
const userCount = 10;
const isAuthenticated = true;
const maxRetryAttempts = 3;

// Bad
const uc = 10;
const auth = true;
const max = 3;
```

### Constants

**Convention:** [UPPER_SNAKE_CASE, SCREAMING_SNAKE_CASE]

**Examples:**
```javascript
const MAX_CONNECTIONS = 100;
const API_BASE_URL = "https://api.example.com";
const DEFAULT_TIMEOUT = 5000;
```

### Functions/Methods

**Convention:** [camelCase for most languages, snake_case for Python]

**Examples:**
```javascript
// Good - Verb-based, descriptive names
function calculateTotal() { }
function getUserById(id) { }
function isValidEmail(email) { }

// Bad - Unclear or non-descriptive
function calc() { }
function get(id) { }
function check(email) { }
```

### Classes

**Convention:** [PascalCase/UpperCamelCase]

**Examples:**
```javascript
// Good
class UserAccount { }
class PaymentProcessor { }
class ValidationError { }

// Bad
class userAccount { }
class paymentprocessor { }
class validationerror { }
```

### Files and Directories

**Convention:** [kebab-case, snake_case, PascalCase for classes]

**Examples:**
```
// Good
user-account.js
payment-processor.js
validation-error.js

// Or for class files
UserAccount.js
PaymentProcessor.js
ValidationError.js
```

---

## Code Organization

### File Structure

**Recommended Order:**
1. Imports/Dependencies
2. Constants
3. Type definitions/Interfaces
4. Class or function definitions
5. Exports

**Example:**
```javascript
// 1. Imports
import { someModule } from './some-module';

// 2. Constants
const MAX_ITEMS = 100;

// 3. Type definitions
interface User {
  id: string;
  name: string;
}

// 4. Class/function definitions
class UserService {
  // implementation
}

// 5. Exports
export { UserService };
```

### Module Size

- **Guideline:** Keep modules focused and < 300 lines when possible
- **Single Responsibility:** Each module should have one clear purpose
- **Refactoring:** Split large modules into smaller, cohesive units

---

## Comments and Documentation

### When to Comment

**Do Comment:**
- Complex algorithms or business logic
- Non-obvious decisions or trade-offs
- Public APIs and interfaces
- TODOs and known issues

**Don't Comment:**
- Obvious code that is self-explanatory
- To compensate for bad naming or structure
- To explain what the code does (code should show this)

### Comment Style

**Single-Line Comments:**
```javascript
// Good - Explain why, not what
// Using exponential backoff to prevent API rate limiting
const retryDelay = baseDelay * Math.pow(2, attemptCount);

// Bad - States the obvious
// Multiply baseDelay by 2 to the power of attemptCount
const retryDelay = baseDelay * Math.pow(2, attemptCount);
```

**Multi-Line Comments:**
```javascript
/**
 * Processes user payment using the configured payment provider.
 *
 * @param {string} userId - The unique identifier of the user
 * @param {number} amount - The payment amount in cents
 * @returns {Promise<PaymentResult>} The payment processing result
 * @throws {PaymentError} If payment processing fails
 */
async function processPayment(userId, amount) {
  // implementation
}
```

### Documentation Comments

Use standard documentation formats for your language:
- **JavaScript/TypeScript:** JSDoc
- **Python:** Docstrings (Google, NumPy, or Sphinx style)
- **Java:** Javadoc
- **C#:** XML Documentation Comments

---

## Language-Specific Guidelines

### [Language 1: e.g., JavaScript/TypeScript]

**Specific Conventions:**
- Use `const` by default, `let` when reassignment is needed, avoid `var`
- Prefer arrow functions for callbacks
- Use template literals for string interpolation
- Prefer async/await over raw promises

**Example:**
```javascript
// Good
const users = await fetchUsers();
const message = `Found ${users.length} users`;

// Bad
var users = fetchUsers().then(u => u);
var message = 'Found ' + users.length + ' users';
```

### [Language 2: e.g., Python]

**Specific Conventions:**
- Follow PEP 8 style guide
- Use type hints for function signatures
- Prefer list comprehensions for simple transformations
- Use context managers for resource management

**Example:**
```python
# Good
def get_user_names(users: list[User]) -> list[str]:
    return [user.name for user in users]

# Bad
def getUserNames(users):
    result = []
    for user in users:
        result.append(user.name)
    return result
```

---

## Linting and Formatting Tools

### Automated Tools

**Linter:** [e.g., ESLint, Pylint, RuboCop]
**Formatter:** [e.g., Prettier, Black, gofmt]

### Configuration

**Setup:**
```bash
# Install linter and formatter
[INSTALL_COMMAND]

# Run linter
[LINT_COMMAND]

# Run formatter
[FORMAT_COMMAND]
```

### Pre-commit Hooks

Install pre-commit hooks to automatically check code style:

```bash
# Install pre-commit
[INSTALL_PRECOMMIT_COMMAND]

# Set up hooks
[SETUP_HOOKS_COMMAND]
```

### IDE Integration

**Recommended Settings:**
- Enable format on save
- Show linting errors inline
- Auto-fix issues when possible

---

## Code Review Standards

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Naming is clear and consistent
- [ ] Functions are focused and single-purpose
- [ ] Complex logic includes explanatory comments
- [ ] No unnecessary code or commented-out blocks
- [ ] Tests are included and passing
- [ ] Documentation is updated if needed

### Common Issues

- **Magic Numbers:** Replace with named constants
- **Long Functions:** Break into smaller functions
- **Nested Conditionals:** Refactor with early returns or separate functions
- **Duplicate Code:** Extract into reusable functions

---

## Related Documentation

- [README](../../README.md): Project overview and documentation index
- [Development Guide](./dev-abstract.md): Development processes and standards
- [Architecture Overview](./architecture.md): System design and patterns
- [Testing Guide](./testing-abstract.md): Testing standards and practices
- [Documentation Guide](./documentation-abstract.md): Documentation standards
