# LaVidaLuca Backend Testing Documentation

This document provides comprehensive information about the testing infrastructure for the LaVidaLuca backend application.

## Table of Contents

1. [Test Architecture](#test-architecture)
2. [Test Types](#test-types)
3. [Running Tests](#running-tests)
4. [Test Coverage](#test-coverage)
5. [Performance Testing](#performance-testing)
6. [Security Testing](#security-testing)
7. [CI/CD Integration](#cicd-integration)
8. [Writing Tests](#writing-tests)
9. [Test Data Management](#test-data-management)
10. [Troubleshooting](#troubleshooting)

## Test Architecture

The testing infrastructure is built using:

- **pytest** - Main testing framework
- **pytest-asyncio** - Async test support
- **pytest-cov** - Coverage reporting
- **httpx** - HTTP client for API testing
- **factory-boy** - Test data generation
- **locust** - Performance/load testing
- **bandit** - Security scanning
- **safety** - Vulnerability scanning

### Test Structure

```
apps/backend/app/tests/
├── conftest.py                 # Test configuration and fixtures
├── factories.py               # Test data factories
├── utils.py                   # Test utilities and helpers
├── test_auth_comprehensive.py # Authentication tests
├── test_database_integration.py # Database integration tests
├── test_api_endpoints.py      # API endpoint tests
├── test_security.py           # Security tests
├── test_performance.py        # Performance tests (Locust)
├── test_auth.py               # Basic auth tests (existing)
├── test_activities.py         # Activity tests (existing)
└── test_main.py               # Main app tests (existing)
```

## Test Types

### 1. Unit Tests
Test individual functions and methods in isolation.

**Markers**: `@pytest.mark.unit`

**Examples**:
- Password hashing functions
- JWT token creation/validation
- Data validation functions
- Utility functions

### 2. Integration Tests
Test interactions between different components.

**Markers**: `@pytest.mark.integration`

**Examples**:
- Database CRUD operations
- Authentication flows
- API endpoint interactions
- Service layer integration

### 3. Security Tests
Test security measures and vulnerability prevention.

**Markers**: `@pytest.mark.security`

**Examples**:
- SQL injection prevention
- XSS protection
- Authentication bypass attempts
- Input validation
- Rate limiting

### 4. Performance Tests
Test application performance under load.

**Markers**: `@pytest.mark.performance`

**Examples**:
- Load testing with multiple users
- Stress testing under high load
- Endpoint response time benchmarks
- Database performance under load

## Running Tests

### Quick Start

```bash
# Run all tests
cd apps/backend
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test types
pytest -m "unit"
pytest -m "integration"
pytest -m "security"
```

### Using the Test Runner Script

```bash
# Run all tests with coverage
./run_tests.sh

# Run only unit tests
./run_tests.sh --unit-only

# Run only integration tests
./run_tests.sh --integration-only

# Run only security tests
./run_tests.sh --security-only

# Include performance tests
./run_tests.sh --performance

# Skip coverage reporting
./run_tests.sh --no-coverage

# Stop on first failure
./run_tests.sh --fail-fast

# Verbose output
./run_tests.sh --verbose
```

### Performance Testing

Performance tests use Locust and should be run separately:

```bash
# Start the application
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run performance tests
locust -f app/tests/test_performance.py --host=http://localhost:8000

# Headless performance test
locust -f app/tests/test_performance.py --host=http://localhost:8000 \
       --users 50 --spawn-rate 5 --run-time 60s --headless
```

## Test Coverage

### Coverage Configuration

Coverage is configured in `.coveragerc`:

- **Target**: 80% minimum coverage
- **Reports**: HTML, XML, and terminal
- **Exclusions**: Test files, migrations, `__pycache__`

### Coverage Reports

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html
# View at htmlcov/index.html

# Generate XML coverage report (for CI)
pytest --cov=app --cov-report=xml

# Terminal coverage report
pytest --cov=app --cov-report=term-missing
```

### Coverage Thresholds

- **Minimum overall coverage**: 80%
- **Critical paths**: 95% (auth, security)
- **New code**: 100% coverage required

## Performance Testing

### Load Testing Scenarios

1. **Normal Load**: 10-50 concurrent users
2. **High Load**: 100-200 concurrent users  
3. **Stress Test**: 500+ concurrent users until failure
4. **Spike Test**: Sudden load increases

### Performance Metrics

- **Response Time**: < 200ms for simple endpoints
- **Throughput**: > 100 requests/second
- **Error Rate**: < 1% under normal load
- **Resource Usage**: Memory and CPU monitoring

### Performance Test Classes

```python
# Mixed user behavior
LaVidaLucaUser

# Authenticated users only
AuthenticatedUser

# High-frequency requests
StressTestUser

# Endpoint-specific benchmarks
EndpointBenchmarkUser

# Database stress testing
DatabaseStressUser
```

## Security Testing

### Security Test Categories

1. **Authentication Security**
   - Token validation
   - Session management
   - Password security

2. **Input Validation**
   - SQL injection prevention
   - XSS protection
   - Command injection prevention
   - Path traversal prevention

3. **Rate Limiting**
   - Login attempt limiting
   - API rate limiting
   - Brute force protection

4. **Data Exposure**
   - Sensitive data in responses
   - Error message information disclosure
   - Internal ID exposure

### Security Scanning

```bash
# Run security tests
pytest -m security

# Bandit security scan
bandit -r app/

# Safety vulnerability check
safety check

# Combined security scan
./run_tests.sh --security-scan
```

## CI/CD Integration

### GitHub Actions Workflow

The CI pipeline includes:

1. **Multi-version Testing**: Python 3.9, 3.10, 3.11, 3.12
2. **Test Matrix**: Unit, Integration, Security tests
3. **Code Quality**: Linting, formatting, type checking
4. **Security Scanning**: Bandit, Safety
5. **Coverage Reporting**: Codecov integration
6. **Performance Testing**: On main/develop branches
7. **Artifact Collection**: Test reports, coverage

### Workflow Configuration

```yaml
# .github/workflows/backend.yml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11', '3.12']
    test-type: ['unit', 'integration', 'security']
```

### Environment Variables

Required for CI:

```bash
ENVIRONMENT=testing
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test_lavidaluca
JWT_SECRET_KEY=test-secret-key-for-ci
OPENAI_API_KEY=test-key
REDIS_URL=redis://localhost:6379/0
```

## Writing Tests

### Test Naming Convention

```python
# Test files
test_*.py

# Test classes
class TestUserAuthentication:

# Test methods
def test_user_registration_success():
def test_user_registration_duplicate_email():
def test_login_invalid_credentials():
```

### Test Structure

```python
import pytest
from app.tests.factories import UserFactory
from app.tests.utils import AuthTestHelper

class TestUserOperations:
    def setup_method(self):
        """Set up test data."""
        self.auth_helper = AuthTestHelper(client)
    
    def test_operation_success(self, client, db_session):
        """Test successful operation."""
        # Arrange
        user = UserFactory()
        
        # Act
        response = client.get("/endpoint")
        
        # Assert
        assert response.status_code == 200
        
    def test_operation_failure(self, client):
        """Test operation failure."""
        # Test failure scenario
        pass
```

### Using Factories

```python
from app.tests.factories import UserFactory, ActivityFactory

# Create a user
user = UserFactory()

# Create a user with specific attributes
admin = UserFactory(is_superuser=True)

# Create user with activities
user, activities = create_user_with_activities(num_activities=5)

# Batch creation
users = BatchUserFactory.create_batch(size=10)
```

### Using Test Helpers

```python
from app.tests.utils import AuthTestHelper, APITestHelper

def test_authenticated_endpoint(client):
    auth_helper = AuthTestHelper(client)
    api_helper = APITestHelper(client)
    
    # Create and login user
    user_data, token = auth_helper.create_and_login_user()
    headers = auth_helper.get_auth_headers(user_data["email"])
    
    # Test API endpoint
    response = client.get("/api/v1/protected", headers=headers)
    api_helper.assert_success_response(response)
```

### Async Tests

```python
@pytest.mark.asyncio
async def test_async_operation(db_session):
    """Test async database operation."""
    user = User(email="test@example.com")
    db_session.add(user)
    await db_session.commit()
    
    result = await db_session.execute(select(User))
    assert result.scalar_one() == user
```

## Test Data Management

### Test Database

Tests use a separate test database:

- **Development**: SQLite in-memory or file
- **CI**: PostgreSQL test database
- **Isolation**: Each test gets clean database state

### Data Factories

Use Factory Boy for consistent test data:

```python
# Simple factory usage
user = UserFactory()

# Custom attributes
user = UserFactory(email="specific@example.com")

# Batch creation
users = UserFactory.create_batch(5)

# Related objects
user, activities = create_user_with_activities(3)
```

### Data Cleanup

Tests automatically clean up data:

- Transaction rollback in fixtures
- Database truncation between tests
- Temporary file cleanup

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   ```bash
   # Check PostgreSQL is running
   pg_isready -h localhost -p 5432
   
   # Check environment variables
   echo $DATABASE_URL
   ```

2. **Import Errors**
   ```bash
   # Ensure you're in the backend directory
   cd apps/backend
   
   # Check Python path
   export PYTHONPATH=.
   ```

3. **Async Test Issues**
   ```python
   # Ensure proper async markers
   @pytest.mark.asyncio
   async def test_async_function():
       pass
   ```

4. **Coverage Issues**
   ```bash
   # Clear previous coverage data
   rm .coverage
   
   # Ensure coverage is tracking the right files
   pytest --cov=app --cov-report=term
   ```

### Debug Mode

Run tests in debug mode:

```bash
# Verbose output
pytest -v -s

# Drop into debugger on failure
pytest --pdb

# Show local variables in traceback
pytest -l
```

### Performance Issues

If tests are slow:

```bash
# Show slowest tests
pytest --durations=10

# Run tests in parallel
pytest -n auto

# Profile test execution
pytest --profile
```

### Memory Issues

For memory-intensive tests:

```bash
# Monitor memory usage
pytest --memory-profile

# Run tests with memory limits
pytest --maxfail=1
```

## Best Practices

### Test Organization

1. **Group related tests** in classes
2. **Use descriptive names** for test methods
3. **Keep tests independent** - no shared state
4. **Use appropriate markers** for test categorization

### Test Data

1. **Use factories** for consistent data generation
2. **Avoid hardcoded values** when possible
3. **Clean up** test data properly
4. **Use realistic data** for better test coverage

### Assertions

1. **Use specific assertions** - avoid generic `assert True`
2. **Test both success and failure** cases
3. **Check side effects** - database changes, logs, etc.
4. **Validate response schemas** for API tests

### Performance

1. **Keep tests fast** - under 5 seconds each
2. **Use database transactions** for isolation
3. **Mock external services** to avoid network calls
4. **Run expensive tests separately** with markers

## Contributing

When adding new tests:

1. **Follow naming conventions**
2. **Add appropriate markers**
3. **Update documentation** if needed
4. **Ensure tests pass** in CI
5. **Maintain coverage thresholds**

For questions or issues with testing, please refer to the project's issue tracker or contact the development team.