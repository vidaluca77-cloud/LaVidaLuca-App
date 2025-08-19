# LaVidaLuca Backend Test Suite

This directory contains a comprehensive test suite for the LaVidaLuca Backend API, covering unit tests, integration tests, database tests, performance tests, and security tests.

## Test Structure

### Test Files

- **`conftest.py`** - Test configuration, fixtures, and factories
- **`test_api.py`** - Comprehensive API integration tests
- **`test_db.py`** - Database model and query tests
- **`test_services.py`** - Unit tests for service layer components
- **`test_performance.py`** - Performance and load testing
- **`test_security.py`** - Security and authentication tests

### Test Categories

#### 1. Unit Tests (`test_services.py`)
- **Security Service Tests**: Password hashing, JWT token handling, authentication
- **OpenAI Service Tests**: AI integration, suggestion generation, content analysis
- **Activity Service Tests**: Activity filtering, recommendations, matching algorithms
- **User Service Tests**: User management, profile updates, authentication
- **Validation Service Tests**: Input validation, sanitization, security checks
- **Cache Service Tests**: Caching operations, key generation

#### 2. Integration Tests (`test_api.py`)
- **Health & Root Endpoints**: Basic connectivity and status checks
- **Authentication API**: User registration, login, token validation
- **Activities API**: CRUD operations, filtering, pagination, authorization
- **Users API**: User management endpoints
- **Error Handling**: Invalid requests, malformed data, edge cases
- **Rate Limiting**: Concurrent request handling

#### 3. Database Tests (`test_db.py`)
- **Model Tests**: User, Activity, ActivitySuggestion models
- **Constraint Tests**: Unique constraints, foreign keys, required fields
- **Relationship Tests**: Model associations and joins
- **Query Tests**: Complex queries, filtering, pagination, aggregations
- **Transaction Tests**: Rollback behavior, nested transactions
- **Performance Tests**: Bulk operations, query optimization

#### 4. Performance Tests (`test_performance.py`)
- **API Performance**: Response time measurement, endpoint efficiency
- **Concurrent Load**: Multi-threaded request handling
- **Database Performance**: Query optimization, bulk operations
- **Memory Usage**: Memory leak detection, resource management
- **Scalability**: Performance under increasing load
- **Response Time Consistency**: Variance and reliability testing

#### 5. Security Tests (`test_security.py`)
- **Authentication Security**: Credential validation, brute force protection
- **Authorization**: Access control, permission verification
- **Input Validation**: XSS prevention, SQL injection protection
- **Data Leakage Prevention**: Sensitive information exposure
- **Session Security**: Token management, expiration handling
- **Rate Limiting**: DoS protection, abuse prevention
- **Transport Security**: HTTPS, security headers

## Test Configuration

### Pytest Configuration (`pytest.ini`)
```ini
[tool:pytest]
testpaths = tests app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=80
asyncio_mode = auto
markers =
    unit: Unit tests
    integration: Integration tests  
    performance: Performance tests
    security: Security tests
    slow: Slow running tests
    db: Database tests
```

### Test Fixtures

The test suite uses comprehensive fixtures defined in `conftest.py`:

- **Database Fixtures**: `db_session`, `setup_test_db`
- **Model Factories**: `UserFactory`, `ActivityFactory`, `ActivitySuggestionFactory`
- **Authentication Fixtures**: `auth_headers`, `superuser_auth_headers`, `expired_token`
- **Test Data Fixtures**: `test_user`, `test_activity`, `test_activities`, `multiple_users`
- **Sample Data Fixtures**: `sample_user_data`, `sample_activity_data`

## Running Tests

### Run All Tests
```bash
cd apps/backend
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Performance tests only
pytest -m performance

# Security tests only
pytest -m security

# Database tests only
pytest -m db
```

### Run Specific Test Files
```bash
# API tests
pytest tests/test_api.py

# Database tests
pytest tests/test_db.py

# Service tests
pytest tests/test_services.py

# Performance tests
pytest tests/test_performance.py

# Security tests
pytest tests/test_security.py
```

### Run with Coverage
```bash
# Generate coverage report
pytest --cov=app --cov-report=html --cov-report=term-missing

# View HTML coverage report
open htmlcov/index.html
```

### Run Tests in Parallel
```bash
# Run tests in parallel using pytest-xdist
pytest -n auto
```

## Test Data Management

### Database Setup
- Tests use SQLite in-memory database for isolation
- Each test gets a fresh database session
- Database is automatically cleaned up after each test
- Test data is created using Factory Boy factories

### Test Isolation
- Each test function gets its own database transaction
- Database state is rolled back after each test
- No test dependencies or shared state
- Parallel test execution safe

## Performance Benchmarks

### Expected Performance Targets
- **Health endpoint**: < 100ms response time
- **Activity list**: < 500ms response time
- **User login**: < 500ms response time
- **Activity creation**: < 1 second
- **Concurrent requests**: Handle 20+ simultaneous requests
- **Database queries**: Complex queries < 500ms

### Memory Usage
- **Large responses**: < 50MB memory increase
- **Repeated requests**: < 10MB memory growth (leak detection)

## Security Testing Coverage

### Authentication & Authorization
- ✅ Password hashing and verification
- ✅ JWT token generation and validation
- ✅ Token expiration handling
- ✅ Malformed token rejection
- ✅ Brute force protection
- ✅ Access control and permissions

### Input Validation
- ✅ XSS prevention
- ✅ SQL injection protection
- ✅ Large payload handling
- ✅ Invalid JSON handling
- ✅ File upload security (if applicable)

### Data Protection
- ✅ Password exposure prevention
- ✅ Sensitive data leakage checks
- ✅ Error message information disclosure
- ✅ Debug information exposure

## Continuous Integration

### Test Automation
The test suite is designed for CI/CD integration:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    cd apps/backend
    pip install -r requirements.txt
    pytest --cov=app --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v1
  with:
    file: ./apps/backend/coverage.xml
```

## Test Dependencies

Additional testing dependencies are included in `requirements.txt`:

```txt
# Testing & Development
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
pytest-xdist==3.5.0
httpx==0.25.2
factory-boy==3.3.0
coverage==7.3.2
psutil==5.9.6
```

## Contributing to Tests

### Adding New Tests
1. Follow the existing test structure and naming conventions
2. Use appropriate pytest markers (`@pytest.mark.unit`, etc.)
3. Create reusable fixtures for complex test data
4. Ensure tests are isolated and don't depend on external state
5. Add performance and security tests for new features

### Test Guidelines
- **Arrange-Act-Assert**: Structure tests clearly
- **Descriptive Names**: Test names should describe what's being tested
- **Single Responsibility**: Each test should test one specific behavior
- **Mock External Dependencies**: Don't rely on external services
- **Test Edge Cases**: Include error conditions and boundary cases

## Coverage Goals

- **Overall Coverage**: > 80%
- **Critical Paths**: > 95% (authentication, data persistence)
- **Security Features**: 100%
- **API Endpoints**: > 90%
- **Service Layer**: > 85%

## Troubleshooting

### Common Issues

1. **Database Connection Errors**: Ensure SQLite is available
2. **Import Errors**: Check PYTHONPATH includes the app directory
3. **Fixture Conflicts**: Use fresh fixtures for each test
4. **Async Test Issues**: Ensure proper async/await usage
5. **Mock Issues**: Reset mocks between tests

### Debug Mode
```bash
# Run tests with detailed output
pytest -v -s

# Run specific test with pdb
pytest -v -s tests/test_api.py::TestAuthenticationAPI::test_login_user_success --pdb
```

This comprehensive test suite ensures the reliability, security, and performance of the LaVidaLuca Backend API, enabling confident deployment and continuous development.