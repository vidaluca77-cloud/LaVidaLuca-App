"""
Test utilities and helper functions for LaVidaLuca backend tests.

Provides common utilities for test setup, data creation, and assertions.
"""

import asyncio
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from contextlib import asynccontextmanager
import tempfile
import os

from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.auth.jwt_handler import create_access_token
from app.models.user import User
from app.models.activity import Activity


class TestTimer:
    """Context manager for timing test operations."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"{self.name} took {duration:.3f} seconds")
    
    @property
    def duration(self) -> float:
        """Get the duration of the timed operation."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


class DatabaseTestHelper:
    """Helper class for database operations in tests."""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def clear_all_tables(self):
        """Clear all tables for test isolation."""
        # Get all table names
        result = await self.db_session.execute(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        tables = result.scalars().all()
        
        # Disable foreign key checks and truncate tables
        for table in tables:
            if table not in ['alembic_version']:  # Skip migration table
                await self.db_session.execute(text(f"TRUNCATE TABLE {table} CASCADE"))
        
        await self.db_session.commit()
    
    async def count_records(self, model_class) -> int:
        """Count records in a table."""
        result = await self.db_session.execute(
            text(f"SELECT COUNT(*) FROM {model_class.__tablename__}")
        )
        return result.scalar()
    
    async def get_all_records(self, model_class):
        """Get all records from a table."""
        from sqlalchemy import select
        result = await self.db_session.execute(select(model_class))
        return result.scalars().all()


class AuthTestHelper:
    """Helper class for authentication-related test operations."""
    
    def __init__(self, client: TestClient):
        self.client = client
        self.tokens = {}
        self.users = {}
    
    def create_test_user(self, email: str = None, password: str = None, **kwargs) -> Dict[str, Any]:
        """Create a test user and return user data."""
        if not email:
            email = f"test_{int(time.time())}@example.com"
        if not password:
            password = "TestPassword123!"
        
        user_data = {
            "email": email,
            "password": password,
            "first_name": kwargs.get("first_name", "Test"),
            "last_name": kwargs.get("last_name", "User"),
            **kwargs
        }
        
        response = self.client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 201, f"User creation failed: {response.text}"
        
        return user_data
    
    def login_user(self, email: str, password: str) -> str:
        """Login user and return access token."""
        login_data = {"email": email, "password": password}
        response = self.client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200, f"Login failed: {response.text}"
        
        token = response.json()["data"]["access_token"]
        self.tokens[email] = token
        return token
    
    def get_auth_headers(self, email: str) -> Dict[str, str]:
        """Get authorization headers for a user."""
        if email not in self.tokens:
            # Try to use the user's password from users dict
            if email in self.users:
                self.login_user(email, self.users[email]["password"])
            else:
                raise ValueError(f"No token found for user {email}")
        
        return {"Authorization": f"Bearer {self.tokens[email]}"}
    
    def create_and_login_user(self, email: str = None, **kwargs) -> tuple[Dict[str, Any], str]:
        """Create user and login, return user data and token."""
        user_data = self.create_test_user(email=email, **kwargs)
        token = self.login_user(user_data["email"], user_data["password"])
        self.users[user_data["email"]] = user_data
        return user_data, token
    
    def create_admin_user(self) -> tuple[Dict[str, Any], str]:
        """Create an admin user and return user data and token."""
        return self.create_and_login_user(
            email=f"admin_{int(time.time())}@example.com",
            is_superuser=True
        )


class APITestHelper:
    """Helper class for API testing operations."""
    
    def __init__(self, client: TestClient):
        self.client = client
        self.auth_helper = AuthTestHelper(client)
    
    def assert_success_response(self, response, expected_status: int = 200):
        """Assert that response is successful."""
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}: {response.text}"
        data = response.json()
        assert data.get("success") is True, f"Response not successful: {data}"
        return data
    
    def assert_error_response(self, response, expected_status: int = 400):
        """Assert that response is an error."""
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}: {response.text}"
        data = response.json()
        assert data.get("success") is False, f"Response should not be successful: {data}"
        return data
    
    def create_test_activity(self, headers: Dict[str, str], **kwargs) -> Dict[str, Any]:
        """Create a test activity and return the response data."""
        activity_data = {
            "title": kwargs.get("title", "Test Activity"),
            "description": kwargs.get("description", "Test activity description"),
            "category": kwargs.get("category", "test"),
            "difficulty_level": kwargs.get("difficulty_level", "beginner"),
            "estimated_duration": kwargs.get("estimated_duration", 30),
            "materials": kwargs.get("materials", ["Test material"]),
            "instructions": kwargs.get("instructions", ["Step 1: Do something"]),
            "tags": kwargs.get("tags", ["test"])
        }
        
        response = self.client.post("/api/v1/activities/", json=activity_data, headers=headers)
        return self.assert_success_response(response, 201)
    
    def get_activity_list(self, **params) -> List[Dict[str, Any]]:
        """Get list of activities with optional parameters."""
        response = self.client.get("/api/v1/activities/", params=params)
        data = self.assert_success_response(response)
        return data["data"]
    
    def check_endpoint_requires_auth(self, method: str, endpoint: str, **kwargs):
        """Check that an endpoint requires authentication."""
        response = getattr(self.client, method.lower())(endpoint, **kwargs)
        assert response.status_code == 401, f"{method} {endpoint} should require authentication"


class PerformanceTestHelper:
    """Helper class for performance testing operations."""
    
    def __init__(self):
        self.measurements = []
    
    def measure_endpoint_performance(self, client: TestClient, method: str, endpoint: str, 
                                   iterations: int = 10, **kwargs) -> Dict[str, float]:
        """Measure endpoint performance over multiple iterations."""
        times = []
        
        for _ in range(iterations):
            start_time = time.time()
            response = getattr(client, method.lower())(endpoint, **kwargs)
            end_time = time.time()
            
            # Only count successful responses
            if response.status_code < 400:
                times.append(end_time - start_time)
        
        if not times:
            raise ValueError("No successful requests to measure")
        
        return {
            "min": min(times),
            "max": max(times),
            "avg": sum(times) / len(times),
            "total": sum(times),
            "count": len(times)
        }
    
    def assert_performance_threshold(self, performance_data: Dict[str, float], 
                                   max_avg_time: float = 1.0, max_single_time: float = 2.0):
        """Assert that performance meets thresholds."""
        assert performance_data["avg"] < max_avg_time, \
            f"Average response time {performance_data['avg']:.3f}s exceeds threshold {max_avg_time}s"
        assert performance_data["max"] < max_single_time, \
            f"Max response time {performance_data['max']:.3f}s exceeds threshold {max_single_time}s"


class SecurityTestHelper:
    """Helper class for security testing operations."""
    
    @staticmethod
    def get_sql_injection_payloads() -> List[str]:
        """Get common SQL injection payloads."""
        return [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO users (email) VALUES ('hacked@evil.com'); --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "admin'/*",
            "' OR 1=1#",
            "1' AND (SELECT COUNT(*) FROM users) > 0 --"
        ]
    
    @staticmethod
    def get_xss_payloads() -> List[str]:
        """Get common XSS payloads."""
        return [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
            "'><script>alert('xss')</script>",
            "\"><script>alert('xss')</script>",
            "<iframe src='javascript:alert(\"xss\")'></iframe>",
            "<body onload=alert('xss')>"
        ]
    
    @staticmethod
    def get_command_injection_payloads() -> List[str]:
        """Get common command injection payloads."""
        return [
            "; ls -la",
            "| cat /etc/passwd",
            "&& rm -rf /",
            "`whoami`",
            "$(cat /etc/passwd)",
            "; cat /etc/passwd",
            "|| id",
            "&& echo vulnerable"
        ]
    
    def test_input_validation(self, client: TestClient, endpoint: str, field: str, 
                            payloads: List[str], method: str = "post", **kwargs):
        """Test input validation against malicious payloads."""
        results = []
        
        for payload in payloads:
            data = kwargs.get("json", {}).copy()
            data[field] = payload
            
            response = getattr(client, method.lower())(endpoint, json=data, **kwargs)
            
            # Should not return 500 (server error)
            assert response.status_code != 500, \
                f"Payload '{payload}' caused server error: {response.text}"
            
            results.append({
                "payload": payload,
                "status_code": response.status_code,
                "response": response.json() if response.status_code != 500 else None
            })
        
        return results


class TestDataHelper:
    """Helper class for managing test data."""
    
    def __init__(self):
        self.created_files = []
        self.temp_dirs = []
    
    def create_temp_file(self, content: str = "", suffix: str = ".txt") -> str:
        """Create a temporary file for testing."""
        fd, path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'w') as tmp_file:
            tmp_file.write(content)
        
        self.created_files.append(path)
        return path
    
    def create_temp_json_file(self, data: Dict[str, Any]) -> str:
        """Create a temporary JSON file."""
        return self.create_temp_file(json.dumps(data, indent=2), ".json")
    
    def create_temp_dir(self) -> str:
        """Create a temporary directory."""
        temp_dir = tempfile.mkdtemp()
        self.temp_dirs.append(temp_dir)
        return temp_dir
    
    def cleanup(self):
        """Clean up created temporary files and directories."""
        for file_path in self.created_files:
            try:
                os.unlink(file_path)
            except OSError:
                pass
        
        for dir_path in self.temp_dirs:
            try:
                import shutil
                shutil.rmtree(dir_path)
            except OSError:
                pass
        
        self.created_files.clear()
        self.temp_dirs.clear()


# Async context manager for database transactions
@asynccontextmanager
async def db_transaction_rollback(db_session: AsyncSession):
    """Context manager that rolls back database transactions for test isolation."""
    transaction = await db_session.begin()
    try:
        yield db_session
    finally:
        await transaction.rollback()


# Utility functions for common test operations

def wait_for_condition(condition_func, timeout: float = 5.0, interval: float = 0.1):
    """Wait for a condition to become true."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False


def retry_on_failure(max_attempts: int = 3, delay: float = 0.1):
    """Decorator to retry a function on failure."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator


def generate_unique_email() -> str:
    """Generate a unique email for testing."""
    timestamp = int(time.time() * 1000)
    return f"test_{timestamp}@example.com"


def generate_test_jwt_token(user_id: str, email: str, expired: bool = False) -> str:
    """Generate a test JWT token."""
    data = {"sub": user_id, "email": email}
    if expired:
        expires_delta = timedelta(seconds=-3600)  # Expired 1 hour ago
    else:
        expires_delta = timedelta(hours=1)
    
    return create_access_token(data=data, expires_delta=expires_delta)


def assert_dict_contains(actual: Dict[str, Any], expected: Dict[str, Any], 
                        ignore_keys: List[str] = None):
    """Assert that actual dict contains all key-value pairs from expected dict."""
    ignore_keys = ignore_keys or []
    
    for key, value in expected.items():
        if key in ignore_keys:
            continue
        
        assert key in actual, f"Key '{key}' not found in actual dict"
        assert actual[key] == value, f"Key '{key}': expected {value}, got {actual[key]}"


def assert_response_schema(response_data: Dict[str, Any], required_fields: List[str],
                          optional_fields: List[str] = None):
    """Assert that response data matches expected schema."""
    optional_fields = optional_fields or []
    
    # Check required fields
    for field in required_fields:
        assert field in response_data, f"Required field '{field}' missing from response"
    
    # Check that no unexpected fields are present
    expected_fields = set(required_fields + optional_fields)
    actual_fields = set(response_data.keys())
    unexpected_fields = actual_fields - expected_fields
    
    assert not unexpected_fields, f"Unexpected fields in response: {unexpected_fields}"


# Export all helper classes and utilities
__all__ = [
    'TestTimer',
    'DatabaseTestHelper',
    'AuthTestHelper', 
    'APITestHelper',
    'PerformanceTestHelper',
    'SecurityTestHelper',
    'TestDataHelper',
    'db_transaction_rollback',
    'wait_for_condition',
    'retry_on_failure',
    'generate_unique_email',
    'generate_test_jwt_token',
    'assert_dict_contains',
    'assert_response_schema'
]