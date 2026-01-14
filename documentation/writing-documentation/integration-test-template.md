---
project_name: [PROJECT_NAME]
title: Integration Test Template
description: Copy-paste template for integration test examples.
last_updated: [YYYY-MM-DD]
cleardoc_version: 2.3.0
keywords: [testing, integration, template, documentation, examples]
---

# [WORKFLOW_NAME] Integration Tests

**Path:** Documentation > Testing > [WORKFLOW_NAME] Integration Tests

Example integration tests for [WORKFLOW_NAME] workflows following project standards.

## Basic Workflow Test

```javascript
describe('[WORKFLOW_NAME] Workflow', () => {
  beforeAll(async () => {
    // Start test environment
    await setupTestDatabase();
    await loadFixtures(['users.json', 'products.json']);
  });
  
  afterAll(async () => {
    await teardownTestDatabase();
  });
  
  it('should complete full workflow successfully', async () => {
    // Step 1: Initial action
    const [RESULT_ONE] = await [SERVICE_ONE].[METHOD]([INPUT]);
    expect([RESULT_ONE]).toBeDefined();
    
    // Step 2: Intermediate action
    const [RESULT_TWO] = await [SERVICE_TWO].[METHOD]([RESULT_ONE]);
    expect([RESULT_TWO].status).toBe('in_progress');
    
    // Step 3: Final action
    const [RESULT_THREE] = await [SERVICE_THREE].[METHOD]([RESULT_TWO]);
    expect([RESULT_THREE].status).toBe('completed');
  });
});
```

## Testing API Endpoint Integration

```javascript
describe('POST /api/[RESOURCE]', () => {
  it('should create [RESOURCE] and persist to database', async () => {
    const payload = {
      name: '[RESOURCE_NAME]',
      email: '[USER_EMAIL]',
      status: 'active'
    };
    
    const response = await request(app)
      .post('/api/[RESOURCE]')
      .set('Authorization', `Bearer [TEST_TOKEN]`)
      .send(payload);
    
    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();
    
    // Verify data was persisted
    const [RESOURCE] = await db.query('SELECT * FROM [TABLE] WHERE id = ?', [response.body.id]);
    expect([RESOURCE].name).toBe('[RESOURCE_NAME]');
    expect([RESOURCE].status).toBe('active');
  });
});
```

## Testing Service-to-Service Communication

```javascript
describe('[SERVICE_ONE] → [SERVICE_TWO] Integration', () => {
  it('should send message to [SERVICE_TWO] when event occurs', async () => {
    const messageQueue = [QUEUE_CONNECTION];
    const spy = jest.spyOn(messageQueue, 'send');
    
    // Trigger event in Service One
    await [SERVICE_ONE].processOrder([ORDER_DATA]);
    
    // Verify message was sent
    expect(spy).toHaveBeenCalledWith({
      eventType: 'order_created',
      orderId: [EXPECTED_ORDER_ID],
      items: [EXPECTED_ITEMS]
    });
    
    // Process message in Service Two
    const message = spy.mock.calls[0][0];
    const [RESULT] = await [SERVICE_TWO].handleOrderEvent(message);
    expect([RESULT].status).toBe('acknowledged');
  });
});
```

## Testing Database Integration

```javascript
describe('User Repository', () => {
  let testDatabase;
  
  beforeAll(async () => {
    testDatabase = await connectToTestDatabase();
  });
  
  afterEach(async () => {
    // Clean up test data
    await testDatabase.query('DELETE FROM users WHERE id > 1000');
  });
  
  afterAll(async () => {
    await testDatabase.disconnect();
  });
  
  it('should create user and retrieve with relationships', async () => {
    // Create user
    const userId = await userRepo.create({
      name: '[USER_NAME]',
      email: '[USER_EMAIL]'
    });
    
    // Create related records
    await orderRepo.create({
      userId: userId,
      total: 99.99
    });
    
    // Retrieve and verify relationships
    const user = await userRepo.findWithOrders(userId);
    expect(user.name).toBe('[USER_NAME]');
    expect(user.orders).toHaveLength(1);
    expect(user.orders[0].total).toBe(99.99);
  });
});
```

## Testing Message Queue Integration

```javascript
describe('Order Processing Message Queue', () => {
  let messageQueue;
  
  beforeEach(() => {
    messageQueue = [QUEUE_MOCK];
    messageQueue.messages = [];
  });
  
  it('should enqueue and process order event', async () => {
    // Enqueue event
    await messageQueue.send('order_events', {
      orderId: '[ORDER_ID]',
      action: 'created',
      timestamp: new Date().toISOString()
    });
    
    expect(messageQueue.messages).toHaveLength(1);
    
    // Process event
    const message = messageQueue.messages[0];
    const [RESULT] = await orderProcessor.handleEvent(message);
    
    expect([RESULT].processed).toBe(true);
    expect([RESULT].errors).toHaveLength(0);
  });
});
```

## Testing Multi-Step User Journey

```javascript
describe('User Registration Journey', () => {
  it('should complete full registration workflow', async () => {
    // Step 1: Register user
    const registerResponse = await request(app)
      .post('/api/auth/register')
      .send({
        email: '[NEW_USER_EMAIL]',
        password: '[PASSWORD]',
        name: '[USER_NAME]'
      });
    
    expect(registerResponse.status).toBe(201);
    const userId = registerResponse.body.userId;
    
    // Step 2: Verify email was sent
    const emailQueue = [EMAIL_QUEUE];
    expect(emailQueue.messages).toHaveLength(1);
    expect(emailQueue.messages[0].to).toBe('[NEW_USER_EMAIL]');
    
    // Step 3: Login with registered account
    const loginResponse = await request(app)
      .post('/api/auth/login')
      .send({
        email: '[NEW_USER_EMAIL]',
        password: '[PASSWORD]'
      });
    
    expect(loginResponse.status).toBe(200);
    expect(loginResponse.body.token).toBeDefined();
    
    // Step 4: Verify user profile
    const profileResponse = await request(app)
      .get('/api/users/profile')
      .set('Authorization', `Bearer ${loginResponse.body.token}`);
    
    expect(profileResponse.body.email).toBe('[NEW_USER_EMAIL]');
    expect(profileResponse.body.name).toBe('[USER_NAME]');
  });
});
```

---

## Running Integration Tests

```bash
# Run all integration tests
npm run test:integration

# Run specific test suite
npm run test:integration [WORKFLOW_NAME].test.js

# Run with coverage
npm run test:integration -- --coverage

# Run with extended timeout
npm run test:integration -- --testTimeout=10000
```

## Notes

- Integration tests typically run slower due to real/simulated database operations
- Use test fixtures for consistent test data
- Mock external services (email, payments) unless testing their specific integration
- Clean up database state between tests with `afterEach` hooks
