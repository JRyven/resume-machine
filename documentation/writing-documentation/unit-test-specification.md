---
project_name: [PROJECT_NAME]
title: Unit Test Specification
description: Rules for documenting unit test structure, patterns, and examples.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, unit, specification, documentation, patterns]
---

# Unit Test Specification

**Path:** Documentation > Writing Documentation > Unit Test Specification

Unit test documentation defines testing standards, patterns, and conventions for testing individual functions and components.

## Purpose

Unit test documentation:
- Establishes testing conventions and standards
- Defines test structure and naming patterns
- Explains assertion and mock usage
- Provides test coverage expectations
- Demonstrates common testing patterns

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: Unit Testing Standards
description: Standards and patterns for writing unit tests.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, unit, standards, patterns, documentation]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > Testing > Unit Testing Standards
```

### Test Structure

Define the standard structure:

```markdown
## Test Structure

Every unit test should follow the Arrange-Act-Assert pattern:

```javascript
describe('[UNIT_UNDER_TEST]', () => {
  it('should [EXPECTED_BEHAVIOR] when [CONDITION]', () => {
    // Arrange: Set up test data
    const [INPUT] = [INITIALIZATION];
    
    // Act: Call the function under test
    const [RESULT] = [FUNCTION_CALL];
    
    // Assert: Verify the result
    expect([RESULT]).toBe([EXPECTED_VALUE]);
  });
});
```
```

### Naming Conventions

```markdown
## Naming Conventions

- **Test files**: `[UNIT_NAME].test.js` or `[UNIT_NAME].spec.js`
- **Test suites**: Use `describe('[UNIT_NAME]', ...)`
- **Test cases**: Use `it('should [EXPECTED_BEHAVIOR] when [CONDITION]', ...)`
- **Test data**: Use descriptive names like `validInput`, `invalidEmail`, `emptyArray`
```

### Assertion Standards

Document assertion patterns:

```markdown
## Assertions

Standard assertion methods:

- `expect([VALUE]).toBe([EXPECTED])` - Exact equality
- `expect([ARRAY]).toContain([ITEM])` - Array contains item
- `expect([FUNCTION]).toThrow()` - Function throws error
- `expect([VALUE]).toBeNull()` - Value is null
- `expect([VALUE]).toBeDefined()` - Value is defined
```

### Mock and Stub Standards

```markdown
## Mocking

Mock external dependencies:

```javascript
jest.mock('[MODULE_NAME]', () => ({
  [FUNCTION_NAME]: jest.fn().mockReturnValue([MOCK_VALUE])
}));
```

Use `.mockReturnValue()` for return values and `.mockImplementation()` for complex behavior.
```

## Optional Sections

### Code Coverage Requirements

```markdown
## Coverage Requirements

- Overall: Minimum 80% line coverage
- Critical paths: 100% coverage required
- Exclude: Generated code, vendor code
```

### Common Testing Patterns

Demonstrate patterns:

```markdown
## Testing Async Functions

```javascript
it('should resolve with data', async () => {
  const [RESULT] = await [ASYNC_FUNCTION]([INPUT]);
  expect([RESULT]).toEqual([EXPECTED]);
});
```

## Testing Error Cases

```javascript
it('should throw error when [CONDITION]', () => {
  expect(() => [FUNCTION]([INVALID_INPUT])).toThrow([ERROR_TYPE]);
});
```
```

## Example

```markdown
# Unit Testing Standards

**Path:** Documentation > Testing > Unit Testing Standards

Standards for writing unit tests across the codebase.

## Test Structure

All tests follow the Arrange-Act-Assert pattern:

```javascript
describe('calculateTotal', () => {
  it('should sum array of numbers correctly', () => {
    // Arrange
    const numbers = [10, 20, 30];
    
    // Act
    const result = calculateTotal(numbers);
    
    // Assert
    expect(result).toBe(60);
  });
});
```

## Naming Conventions

- **Test files**: `[FUNCTION_NAME].test.js`
- **Describe blocks**: `describe('[FUNCTION_NAME]', ...)`
- **Test cases**: `it('should [BEHAVIOR] when [CONDITION]', ...)`

Example: Test file named `userService.test.js` contains:

```javascript
describe('userService', () => {
  it('should create user with valid data', () => {
    // test code
  });
  
  it('should throw error when email is invalid', () => {
    // test code
  });
});
```

## Assertions

Common assertion patterns:

```javascript
// Exact equality
expect(result).toBe(expected);

// Object/array equality
expect(result).toEqual({id: 1, name: 'Test'});

// Array contains
expect(items).toContain('item');

// Error handling
expect(() => function()).toThrow(Error);

// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
```

## Coverage Requirements

- Minimum 80% line coverage for all code
- 100% coverage for critical functions (authentication, payments, security)
- Exclude generated files and node_modules
```

## Size Guidelines

- Total: 400-600 words
- YAML: ~40 words
- Breadcrumb: 5 words
- Test Structure: 80-120 words
- Naming: 60-100 words
- Assertions: 60-100 words
- Mocking: 60-100 words
- Other sections: Remaining
