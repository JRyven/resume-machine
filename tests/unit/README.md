# Unit Tests

Template placeholder for unit tests.

## Structure

Mirror your source code structure:

```
tests/unit/
├── test_models.py
├── test_services.py
├── test_controllers.py
└── test_utils.py
```

Or organize by feature:

```
tests/unit/
├── auth/
│   ├── test_auth_service.py
│   └── test_password_validator.py
└── users/
    ├── test_user_model.py
    └── test_user_service.py
```

## Mocking and Stubs

Use mocks/stubs for external dependencies:
- Database connections
- API calls
- File system operations
- Third-party services

## Coverage Goals

- **Minimum**: 80% code coverage
- **Target**: 90%+ for critical business logic
- Focus on meaningful tests over coverage numbers

## Testing Principles (SOLID Applied to Tests)

**Single Responsibility**: Each test should verify one behavior.

**DRY**: Extract common setup into fixtures/helpers, but keep test assertions explicit.

**Test Naming**: Use descriptive names that explain what is being tested and expected outcome:
```python
def test_user_service_creates_user_with_valid_data()
def test_password_validator_rejects_short_passwords()
```

## Next Steps

1. Choose testing framework (pytest, jest, testing package, etc.)
2. Configure test runner and coverage tools
3. Write first tests (ideally before implementation - TDD)
4. Set up continuous integration to run tests automatically
5. Remove this placeholder README once tests are added
