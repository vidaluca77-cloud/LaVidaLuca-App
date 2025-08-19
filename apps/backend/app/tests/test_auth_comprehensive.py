"""
Comprehensive authentication flow tests for LaVidaLuca backend.

Tests registration, login, logout, token validation, refresh, and security.
"""

import pytest
import time
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.core.security import create_access_token, verify_token
from app.models.user import User
from app.auth.password import hash_password, verify_password


class TestUserRegistration:
    """Test user registration flow."""

    def test_register_valid_user(self, client: TestClient):
        """Test successful user registration."""
        user_data = {
            "email": "newuser@example.com",
            "password": "SecurePassword123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == user_data["email"]
        assert data["data"]["first_name"] == user_data["first_name"]
        assert data["data"]["last_name"] == user_data["last_name"]
        assert "id" in data["data"]
        assert "hashed_password" not in data["data"]  # Should not expose password

    def test_register_invalid_email(self, client: TestClient):
        """Test registration with invalid email format."""
        user_data = {
            "email": "invalid-email",
            "password": "SecurePassword123!",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "email" in str(data["detail"]).lower()

    def test_register_weak_password(self, client: TestClient):
        """Test registration with weak password."""
        user_data = {
            "email": "user@example.com",
            "password": "123",  # Too weak
            "first_name": "John",
            "last_name": "Doe"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "password" in str(data["detail"]).lower()

    def test_register_missing_required_fields(self, client: TestClient):
        """Test registration with missing required fields."""
        incomplete_data = {
            "email": "user@example.com"
            # Missing password, first_name, last_name
        }
        
        response = client.post("/api/v1/auth/register", json=incomplete_data)
        
        assert response.status_code == 422

    def test_register_duplicate_email(self, client: TestClient, db_session):
        """Test registration with existing email."""
        # First registration
        user_data = {
            "email": "duplicate@example.com",
            "password": "SecurePassword123!",
            "first_name": "First",
            "last_name": "User"
        }
        
        response1 = client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 201
        
        # Second registration with same email
        user_data["first_name"] = "Second"
        response2 = client.post("/api/v1/auth/register", json=user_data)
        
        assert response2.status_code == 400
        data = response2.json()
        assert data["success"] is False
        assert "already registered" in data["detail"].lower()

    def test_register_email_case_insensitive(self, client: TestClient):
        """Test that email registration is case-insensitive."""
        user_data1 = {
            "email": "CaseTest@example.com",
            "password": "SecurePassword123!",
            "first_name": "First",
            "last_name": "User"
        }
        
        user_data2 = {
            "email": "casetest@example.com",  # Same email, different case
            "password": "SecurePassword123!",
            "first_name": "Second",
            "last_name": "User"
        }
        
        response1 = client.post("/api/v1/auth/register", json=user_data1)
        assert response1.status_code == 201
        
        response2 = client.post("/api/v1/auth/register", json=user_data2)
        assert response2.status_code == 400


class TestUserLogin:
    """Test user login flow."""

    def setup_method(self):
        """Set up test user for login tests."""
        self.test_user_data = {
            "email": "logintest@example.com",
            "password": "TestPassword123!",
            "first_name": "Login",
            "last_name": "Test"
        }

    def test_login_valid_credentials(self, client: TestClient):
        """Test successful login with valid credentials."""
        # Register user first
        client.post("/api/v1/auth/register", json=self.test_user_data)
        
        # Login
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "access_token" in data["data"]
        assert data["data"]["token_type"] == "bearer"
        assert "expires_in" in data["data"]
        assert isinstance(data["data"]["expires_in"], int)

    def test_login_invalid_email(self, client: TestClient):
        """Test login with non-existent email."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "AnyPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "incorrect" in data["detail"].lower()

    def test_login_invalid_password(self, client: TestClient):
        """Test login with wrong password."""
        # Register user first
        client.post("/api/v1/auth/register", json=self.test_user_data)
        
        # Login with wrong password
        login_data = {
            "email": self.test_user_data["email"],
            "password": "WrongPassword123!"
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "incorrect" in data["detail"].lower()

    def test_login_email_case_insensitive(self, client: TestClient):
        """Test login with different email case."""
        # Register user
        client.post("/api/v1/auth/register", json=self.test_user_data)
        
        # Login with different case
        login_data = {
            "email": self.test_user_data["email"].upper(),
            "password": self.test_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    def test_login_inactive_user(self, client: TestClient, db_session):
        """Test login with inactive user account."""
        # Register user
        response = client.post("/api/v1/auth/register", json=self.test_user_data)
        user_id = response.json()["data"]["id"]
        
        # Deactivate user
        from sqlalchemy import select, update
        from app.models.user import User
        
        await db_session.execute(
            update(User).where(User.id == user_id).values(is_active=False)
        )
        await db_session.commit()
        
        # Try to login
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        response = client.post("/api/v1/auth/login", json=login_data)
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert "inactive" in data["detail"].lower()

    def test_login_updates_last_login(self, client: TestClient, db_session):
        """Test that login updates last_login timestamp."""
        # Register user
        client.post("/api/v1/auth/register", json=self.test_user_data)
        
        # Get initial last_login
        from sqlalchemy import select
        from app.models.user import User
        
        result = await db_session.execute(
            select(User).where(User.email == self.test_user_data["email"])
        )
        user = result.scalar_one()
        initial_last_login = user.last_login
        
        # Login
        login_data = {
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        }
        
        time.sleep(1)  # Ensure timestamp difference
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        
        # Check updated last_login
        await db_session.refresh(user)
        assert user.last_login is not None
        if initial_last_login:
            assert user.last_login > initial_last_login


class TestTokenValidation:
    """Test JWT token validation and verification."""

    def setup_method(self):
        """Set up test user for token tests."""
        self.test_user_data = {
            "email": "tokentest@example.com",
            "password": "TestPassword123!",
            "first_name": "Token",
            "last_name": "Test"
        }

    def test_verify_valid_token(self, client: TestClient):
        """Test token verification with valid token."""
        # Register and login
        client.post("/api/v1/auth/register", json=self.test_user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": self.test_user_data["email"],
            "password": self.test_user_data["password"]
        })
        
        token = login_response.json()["data"]["access_token"]
        
        # Verify token
        response = client.post(
            "/api/v1/auth/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == self.test_user_data["email"]

    def test_verify_invalid_token(self, client: TestClient):
        """Test token verification with invalid token."""
        invalid_token = "invalid.jwt.token"
        
        response = client.post(
            "/api/v1/auth/verify-token",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False

    def test_verify_expired_token(self, client: TestClient):
        """Test token verification with expired token."""
        # Create expired token
        user_data = {"sub": "test-user-id", "email": "test@example.com"}
        expired_token = create_access_token(
            data=user_data,
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        response = client.post(
            "/api/v1/auth/verify-token",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == 401
        data = response.json()
        assert data["success"] is False
        assert "expired" in data["detail"].lower()

    def test_verify_malformed_token(self, client: TestClient):
        """Test token verification with malformed token."""
        malformed_tokens = [
            "",
            "not.jwt",
            "header.payload",  # Missing signature
            "too.many.parts.here",
            "Bearer token-without-bearer-prefix"
        ]
        
        for token in malformed_tokens:
            response = client.post(
                "/api/v1/auth/verify-token",
                headers={"Authorization": f"Bearer {token}"}
            )
            assert response.status_code == 401

    def test_missing_authorization_header(self, client: TestClient):
        """Test protected endpoint without authorization header."""
        response = client.post("/api/v1/auth/verify-token")
        
        assert response.status_code == 401

    def test_invalid_authorization_scheme(self, client: TestClient):
        """Test with invalid authorization scheme."""
        response = client.post(
            "/api/v1/auth/verify-token",
            headers={"Authorization": "Basic invalid-scheme"}
        )
        
        assert response.status_code == 401


class TestPasswordSecurity:
    """Test password hashing and security."""

    def test_password_hashing(self):
        """Test password hashing functionality."""
        password = "TestPassword123!"
        hashed = hash_password(password)
        
        assert hashed != password  # Password should be hashed
        assert len(hashed) > 20  # Hashed password should be long
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_same_password_different_hashes(self):
        """Test that same password produces different hashes (salt)."""
        password = "TestPassword123!"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        assert hash1 != hash2  # Different salts should produce different hashes
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True

    def test_password_complexity_validation(self, client: TestClient):
        """Test password complexity requirements."""
        weak_passwords = [
            "123",  # Too short
            "password",  # Too simple
            "PASSWORD",  # No lowercase
            "password123",  # No uppercase
            "Password",  # No numbers
            "12345678",  # Only numbers
            "        ",  # Only spaces
        ]
        
        for weak_password in weak_passwords:
            user_data = {
                "email": f"test_{weak_password[:3]}@example.com",
                "password": weak_password,
                "first_name": "Test",
                "last_name": "User"
            }
            
            response = client.post("/api/v1/auth/register", json=user_data)
            assert response.status_code == 422


class TestSecurityHeaders:
    """Test security-related headers and protections."""

    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are properly set."""
        response = client.options("/api/v1/auth/login")
        
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers

    def test_no_sensitive_data_in_responses(self, client: TestClient):
        """Test that sensitive data is not exposed in responses."""
        user_data = {
            "email": "security@example.com",
            "password": "SecurePassword123!",
            "first_name": "Security",
            "last_name": "Test"
        }
        
        # Register user
        response = client.post("/api/v1/auth/register", json=user_data)
        data = response.json()
        
        # Ensure sensitive data is not in response
        assert "password" not in data["data"]
        assert "hashed_password" not in data["data"]
        
        # Login user
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        login_data = login_response.json()
        
        # Token should be present but no sensitive user data
        assert "access_token" in login_data["data"]
        assert "password" not in login_data["data"]
        assert "hashed_password" not in login_data["data"]


class TestConcurrentAuthentication:
    """Test authentication under concurrent load."""

    @pytest.mark.asyncio
    async def test_concurrent_logins(self, client: TestClient):
        """Test concurrent login attempts."""
        import asyncio
        import httpx
        
        # Register user
        user_data = {
            "email": "concurrent@example.com",
            "password": "TestPassword123!",
            "first_name": "Concurrent",
            "last_name": "Test"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Concurrent login attempts
        async def login_attempt():
            async with httpx.AsyncClient(app=client.app, base_url="http://test") as ac:
                response = await ac.post("/api/v1/auth/login", json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                })
                return response.status_code
        
        # Run 10 concurrent login attempts
        tasks = [login_attempt() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        assert all(status == 200 for status in results)

    @pytest.mark.asyncio
    async def test_concurrent_registrations(self, client: TestClient):
        """Test concurrent registration attempts with unique emails."""
        import asyncio
        import httpx
        
        async def register_attempt(user_id: int):
            user_data = {
                "email": f"user{user_id}@example.com",
                "password": "TestPassword123!",
                "first_name": f"User{user_id}",
                "last_name": "Test"
            }
            
            async with httpx.AsyncClient(app=client.app, base_url="http://test") as ac:
                response = await ac.post("/api/v1/auth/register", json=user_data)
                return response.status_code
        
        # Run 10 concurrent registration attempts
        tasks = [register_attempt(i) for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All should succeed
        assert all(status == 201 for status in results)


class TestRateLimitingAndBruteForce:
    """Test protection against brute force attacks and rate limiting."""

    def test_multiple_failed_login_attempts(self, client: TestClient):
        """Test handling of multiple failed login attempts."""
        # Register user
        user_data = {
            "email": "brute@example.com",
            "password": "CorrectPassword123!",
            "first_name": "Brute",
            "last_name": "Test"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Multiple failed attempts
        failed_attempts = 0
        for i in range(10):
            response = client.post("/api/v1/auth/login", json={
                "email": user_data["email"],
                "password": f"WrongPassword{i}"
            })
            if response.status_code == 401:
                failed_attempts += 1
        
        # Should consistently return 401 for wrong passwords
        assert failed_attempts == 10
        
        # Correct password should still work (no account lockout implemented yet)
        response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert response.status_code == 200

    @pytest.mark.skipif(True, reason="Rate limiting not implemented yet")
    def test_api_rate_limiting(self, client: TestClient):
        """Test API rate limiting functionality."""
        # This test would be implemented when rate limiting is added
        pass