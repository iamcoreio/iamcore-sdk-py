# Test Plan for iamcore-sdk-py

## 1. Introduction

This test plan outlines the comprehensive testing strategy for the iamcore-sdk-py project, a Python SDK for interacting with IAM Core APIs. The project has been recently refactored and requires full test coverage to ensure reliability, maintainability, and correctness.

## 2. Test Strategy

### 2.1 Testing Approach
- **Unit Testing**: Test individual functions, methods, and classes in isolation
- **Integration Testing**: Test interactions between components and external API calls
- **Mocking Strategy**: Use pytest-mock or unittest.mock for HTTP requests and external dependencies

### 2.2 Test Coverage Goals
- **Minimum Coverage**: 80% overall code coverage
- **Critical Path Coverage**: 100% coverage for core business logic
- **Branch Coverage**: 90% for conditional statements

## 3. Test Scope

### 3.1 In Scope
- All client classes and their methods
- Model validation and serialization
- Error handling and exception raising
- HTTP request/response handling
- Authentication and authorization flows
- Pagination and search functionality
- IRN (IAM Resource Name) handling

### 3.2 Out of Scope
- External IAM Core API server functionality
- Network connectivity issues
- Third-party library internals (pydantic, requests)

## 4. Test Types

### 4.1 Unit Tests
- Test individual methods in isolation
- Mock HTTP requests and external dependencies
- Test input validation and error conditions
- Test model serialization/deserialization

### 4.2 Integration Tests
- Test full request/response cycles with mocked HTTP responses
- Test client initialization and configuration
- Test complex workflows involving multiple API calls

### 4.3 Edge Case and Error Testing
- Invalid input parameters
- Network timeouts and connection errors
- Malformed API responses
- Authentication failures

## 5. Test Environment

### 5.1 Dependencies
- pytest (already in dev dependencies)
- pytest-cov (already in dev dependencies)
- pytest-mock (to be added)
- responses or httpx-mock for HTTP mocking

### 5.2 Test Data
- Mock API responses in JSON format
- Valid and invalid IRN strings
- Various authentication headers
- Edge case input parameters

## 6. Test Organization

### 6.1 Directory Structure
```
tests/
├── conftest.py                    # Shared fixtures and configuration
├── unit/
│   ├── test_models.py            # Model and DTO tests
│   ├── test_exceptions.py        # Exception handling tests
│   ├── test_http_client.py       # HTTP client tests
│   └── clients/                  # Client-specific unit tests
│       ├── test_auth_client.py
│       ├── test_user_client.py
│       ├── test_policy_client.py
│       ├── test_tenant_client.py
│       ├── test_api_key_client.py
│       ├── test_group_client.py
│       ├── test_resource_client.py
│       ├── test_application_client.py
│       ├── test_app_resource_type_client.py
│       └── test_evaluate_client.py
├── integration/
│   ├── test_main_client.py       # Main Client class integration
│   └── test_workflows.py         # Complex multi-step workflows
└── fixtures/
    ├── mock_responses.py         # Mock API response data
    └── sample_data.py            # Test data generators
```

### 6.2 Naming Conventions
- Test files: `test_*.py`
- Test functions: `test_*`
- Fixtures: `*_fixture` or descriptive names
- Mock objects: `mock_*`

## 7. Test Tools and Frameworks

### 7.1 Primary Tools
- **pytest**: Test runner and framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities

### 7.2 Additional Tools
- **responses**: HTTP response mocking
- **freezegun**: Time mocking if needed
- **faker**: Generate test data

## 8. Key Test Cases

### 8.1 Model Tests
- Pydantic model validation
- Field aliasing (camelCase ↔ snake_case)
- Serialization/deserialization
- Custom converters (IRN handling)

### 8.2 HTTP Client Tests
- Request method construction
- Header handling
- Timeout configuration
- Error response handling

### 8.3 Client-Specific Tests

#### Auth Client
- Token retrieval with valid/invalid credentials
- Error handling for auth failures

#### User Client
- CRUD operations (create, read, update, delete)
- User search and pagination
- Policy attachment/detachment
- Group membership management

#### Policy Client
- Policy CRUD operations
- Policy search functionality

#### Tenant Client
- Tenant management operations
- Issuer retrieval

#### API Key Client
- API key creation and retrieval

#### Group Client
- Group CRUD operations
- Member management
- Policy attachment

#### Resource Client
- Resource CRUD operations
- Bulk operations

#### Application Client
- Application management
- Policy attachment

#### Application Resource Type Client
- Resource type CRUD operations

#### Evaluate Client
- Authorization checks
- Resource evaluation
- Action evaluation

### 8.4 Integration Tests
- Main Client initialization
- End-to-end workflows (e.g., user creation → policy attachment → authorization check)
- Pagination handling across multiple pages

### 8.5 Error Handling Tests
- Network timeouts
- Invalid JSON responses
- Authentication errors
- Validation errors
- Missing required fields

## 9. Test Execution

### 9.1 Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=iamcore --cov-report=term --cov-report=xml

# Run specific test file
pytest tests/unit/clients/test_user_client.py

# Run single test
pytest tests/unit/clients/test_user_client.py::test_create_user
```

### 9.2 CI/CD Integration
- Tests run on GitLab CI
- Coverage reports generated and uploaded
- Minimum coverage thresholds enforced

## 10. Risks and Assumptions

### 10.1 Assumptions
- External IAM Core API contracts remain stable
- Test environment can mock HTTP responses reliably
- All dependencies are compatible with testing framework

### 10.2 Risks
- Complex mocking of HTTP interactions
- Maintaining test data as API evolves
- Ensuring comprehensive coverage of edge cases

### 10.3 Mitigation Strategies
- Use established mocking libraries
- Implement factory functions for test data
- Regular review of test coverage reports
- Pair testing with development to catch gaps early

## 11. Success Criteria

- All tests pass consistently
- Code coverage meets or exceeds targets
- No critical bugs introduced during refactoring
- Tests provide confidence in code changes
- Test suite runs efficiently in CI/CD pipeline

## 12. Maintenance

- Update tests when API contracts change
- Add tests for new features immediately
- Refactor tests alongside code refactoring
- Regularly review and remove obsolete tests

This test plan provides a comprehensive framework for ensuring the reliability and maintainability of the iamcore-sdk-py project. Implementation should follow this plan to achieve thorough test coverage.