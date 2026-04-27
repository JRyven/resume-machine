---
project_name: [PROJECT_NAME]
title: Unit Test Template
description: Copy-paste template for unit test examples.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, unit, template, documentation, examples]
---

# [UNIT_NAME] Tests

**Path:** Documentation > Testing > [UNIT_NAME] Tests

Example unit tests for `[UNIT_NAME]` following project standards.

## Basic Unit Test

```javascript
describe('[FUNCTION_NAME]', () => {
  it('should [EXPECTED_BEHAVIOR] when [CONDITION]', () => {
    // Arrange: Set up test data
    const input = [TEST_INPUT];
    const expected = [EXPECTED_RESULT];

    // Act: Call the function under test
    const result = [FUNCTION_NAME](input);

    // Assert: Verify the result
    expect(result).toBe(expected);
  });
});
```

## Testing with Multiple Assertions

```javascript
describe('[FUNCTION_NAME]', () => {
  it('should [BEHAVIOR_ONE] and [BEHAVIOR_TWO]', () => {
    // Arrange
    const input = [TEST_INPUT];

    // Act
    const result = [FUNCTION_NAME](input);

    // Assert
    expect(result).toHaveProperty('id');
    expect(result).toHaveProperty('name');
    expect(result.status).toBe('active');
  });
});
```

## Testing Error Cases

```javascript
describe('[FUNCTION_NAME]', () => {
  it('should throw error when [INVALID_CONDITION]', () => {
    const invalidInput = [INVALID_VALUE];

    expect(() => {
      [FUNCTION_NAME](invalidInput);
    }).toThrow([ERROR_TYPE]);
  });

  it('should throw specific error message when [CONDITION]', () => {
    const invalidInput = [INVALID_VALUE];

    expect(() => {
      [FUNCTION_NAME](invalidInput);
    }).toThrow('[EXPECTED_ERROR_MESSAGE]');
  });
});
```

## Testing with Mock Dependencies

```javascript
describe('[SERVICE_NAME]', () => {
  beforeEach(() => {
    // Mock external dependency
    jest.mock('[EXTERNAL_MODULE]');
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should call [EXTERNAL_FUNCTION] when [CONDITION]', () => {
    const [MOCKED_MODULE] = require('[EXTERNAL_MODULE]');
    [MOCKED_MODULE].[FUNCTION_NAME].mockReturnValue([MOCK_RETURN_VALUE]);

    [SERVICE_METHOD]([INPUT]);

    expect([MOCKED_MODULE].[FUNCTION_NAME]).toHaveBeenCalledWith([EXPECTED_ARGS]);
  });
});
```

## Testing Async Functions

```javascript
describe('[ASYNC_FUNCTION]', () => {
  it('should resolve with [EXPECTED_DATA] when successful', async () => {
    const input = [TEST_INPUT];
    const expected = [EXPECTED_DATA];

    const result = await [ASYNC_FUNCTION](input);

    expect(result).toEqual(expected);
  });

  it('should reject when [ERROR_CONDITION]', async () => {
    const invalidInput = [INVALID_VALUE];

    await expect([ASYNC_FUNCTION](invalidInput)).rejects.toThrow([ERROR_TYPE]);
  });
});
```

## Testing with Fixtures

```javascript
describe('[MODULE_NAME]', () => {
  let testData;

  beforeAll(() => {
    // Load test fixtures
    testData = require('../fixtures/[RESOURCE].json');
  });

  it('should process [DATA_TYPE] correctly', () => {
    const input = testData.validInput;

    const result = [FUNCTION_NAME](input);

    expect(result).toEqual(testData.expectedOutput);
  });
});
```

## Testing Array Methods

```javascript
describe('[ARRAY_FUNCTION]', () => {
  it('should filter array and return matching items', () => {
    const items = [
      { id: 1, active: true },
      { id: 2, active: false },
      { id: 3, active: true },
    ];

    const result = [FILTER_FUNCTION](items);

    expect(result).toHaveLength(2);
    expect(result).toContainEqual({ id: 1, active: true });
  });
});
```

## Testing Object Creation

```javascript
describe('[CLASS_NAME]', () => {
  it('should create instance with correct properties', () => {
    const instance = new [CLASS_NAME]([CONSTRUCTOR_ARGS]);

    expect(instance.propertyOne).toBe([EXPECTED_VALUE]);
    expect(instance.propertyTwo).toBeDefined();
    expect(instance.method).toBeInstanceOf(Function);
  });
});
```

---

## Running These Tests

```bash
# Run all tests
npm test

# Run specific test file
npm test [UNIT_NAME].test.js

# Run with coverage
npm test -- --coverage

# Run in watch mode (re-run on file change)
npm test -- --watch
```
