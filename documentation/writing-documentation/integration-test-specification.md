---
project_name: [PROJECT_NAME]
title: Integration Test Specification
description: Rules for documenting integration tests that verify component interactions.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, integration, specification, documentation, patterns]
---

# Integration Test Specification

**Path:** Documentation > Writing Documentation > Integration Test Specification

Integration test documentation defines standards for testing interactions between multiple components, services, and systems.

## Purpose

Integration test documentation:
- Establishes multi-component testing patterns
- Defines test environment and fixture setup
- Explains service mocking strategies
- Specifies test data requirements
- Demonstrates workflow testing patterns

## Mandatory Sections

### YAML Front Matter

```yaml
---
project_name: [PROJECT_NAME]
title: Integration Testing Standards
description: Standards and patterns for integration tests.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, integration, standards, patterns, documentation]
---
```

### Breadcrumb Navigation

```markdown
**Path:** Documentation > Testing > Integration Testing Standards
```

### Test Scope Definition

```markdown
## What to Test

Integration tests verify interactions between:
- API endpoints and database
- Services and external APIs
- Message queues and processors
- Multiple microservices
- UI and backend components

**What NOT to test:** Individual functions or components (use unit tests)
```

### Test Environment

Define test infrastructure:

```markdown
## Test Environment

- **Database**: Use test database or in-memory database
- **External Services**: Mock via [MOCK_SERVICE_TOOL] or test doubles
- **Configuration**: Use test configuration file `config.test.js`
- **Fixtures**: Load test data from `fixtures/[RESOURCE].json`
```

### Test Data Management

```markdown
## Test Data

Organize test fixtures:

```
tests/
├── fixtures/
│   ├── users.json
│   ├── orders.json
│   └── products.json
└── integration/
    └── api.test.js
```

Load fixtures in setup:

```javascript
beforeAll(() => {
  const [DATA] = require('../fixtures/[RESOURCE].json');
  // Load data into test database
});
```
```

### Workflow Testing Pattern

```markdown
## Testing Multi-Step Workflows

Test complete workflows across components:

```javascript
describe('User Registration Workflow', () => {
  it('should create user, send email, and return token', async () => {
    // Step 1: Create user via API
    const user = await [API].createUser([USER_DATA]);
    
    // Step 2: Verify email was queued
    expect([EMAIL_QUEUE].called).toBe(true);
    
    // Step 3: Verify token was issued
    expect(user.token).toBeDefined();
  });
});
```
```

## Optional Sections

### Service Mocking Strategy

```markdown
## Mocking External Services

For external services (payment processors, email services):

```javascript
jest.mock('[EXTERNAL_SERVICE]');

[EXTERNAL_SERVICE].processPayment
  .mockResolvedValue({id: '[TRANSACTION_ID]', status: 'success'});
```

Real vs. mocked:
- **Mock**: External APIs, payments, emails
- **Real**: Database, message queues, internal services
```

### Performance Expectations

```markdown
## Performance Baselines

Integration tests should complete within:
- API endpoint tests: < 100ms
- Database operation tests: < 50ms
- Workflow tests: < 1000ms
```

## Example

```markdown
# Integration Testing Standards

**Path:** Documentation > Testing > Integration Testing Standards

Standards for testing component interactions and workflows.

## Test Scope

Integration tests verify interactions between:
- API handlers and database queries
- Services communicating via message queues
- Frontend components and backend APIs
- Multiple microservices in a workflow

**Do NOT use integration tests for:**
- Individual function logic (use unit tests)
- UI rendering behavior (use UI tests)

## Test Environment Setup

```javascript
beforeAll(async () => {
  // Start test database
  await testDatabase.start();
  
  // Load fixtures
  await testDatabase.load('fixtures/users.json');
  
  // Start test server
  await app.listen(3001);
});

afterAll(async () => {
  await testDatabase.stop();
  await app.close();
});
```

## Testing API Workflows

Test complete request-response cycles:

```javascript
describe('User Registration API', () => {
  it('should register user and return auth token', async () => {
    const response = await request(app)
      .post('/api/users/register')
      .send({
        email: 'user@example.com',
        password: '[PASSWORD]',
        name: '[USER_NAME]'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.token).toBeDefined();
    
    // Verify user was created in database
    const user = await User.findOne({email: 'user@example.com'});
    expect(user).toBeDefined();
  });
});
```

## Testing Service Interactions

Test message flows between services:

```javascript
describe('Order Processing Workflow', () => {
  it('should process order and notify warehouse', async () => {
    // Create order via API
    const order = await orderService.create([ORDER_DATA]);
    
    // Verify warehouse notification was sent
    expect(warehouseQueue.send).toHaveBeenCalledWith({
      order_id: order.id,
      items: [ORDER_ITEMS]
    });
  });
});
```

## Performance Expectations

- Single endpoint tests: < 100ms
- Multi-step workflows: < 1 second
- Database-heavy operations: < 500ms
```

## Size Guidelines

- Total: 400-700 words
- YAML: ~40 words
- Breadcrumb: 5 words
- Scope Definition: 60-80 words
- Environment: 80-120 words
- Test Data: 60-100 words
- Workflow Pattern: 80-120 words
- Other sections: Remaining
