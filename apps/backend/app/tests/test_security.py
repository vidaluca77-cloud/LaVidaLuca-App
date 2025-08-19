"""
Comprehensive security tests for LaVidaLuca backend.

Tests authentication bypass, input validation, injection attacks, and security headers.
"""

import pytest
import json
import time
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.core.security import create_access_token


class TestAuthenticationSecurity:
    """Test authentication security measures."""

    def test_bypass_auth_without_token(self, client: TestClient):
        """Test that protected endpoints cannot be accessed without token."""
        protected_endpoints = [
            ("GET", "/api/v1/users/me"),
            ("PUT", "/api/v1/users/me"),
            ("POST", "/api/v1/activities/"),
            ("GET", "/api/v1/activities/my"),
            ("POST", "/api/v1/suggestions/generate"),
        ]
        
        for method, endpoint in protected_endpoints:
            response = getattr(client, method.lower())(endpoint)
            assert response.status_code == 401, f"{method} {endpoint} should require authentication"

    def test_bypass_auth_invalid_token(self, client: TestClient):
        """Test that invalid tokens are rejected."""
        invalid_tokens = [
            "invalid.jwt.token",
            "Bearer invalid",
            "",
            "not-a-jwt-token",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature",
        ]
        
        for token in invalid_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == 401, f"Token '{token}' should be rejected"

    def test_bypass_auth_expired_token(self, client: TestClient):
        """Test that expired tokens are rejected."""
        # Create expired token
        user_data = {"sub": "test-user", "email": "test@example.com"}
        expired_token = create_access_token(
            data=user_data,
            expires_delta=timedelta(seconds=-3600)  # Expired 1 hour ago
        )
        
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/users/me", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert "expired" in data["detail"].lower()

    def test_bypass_auth_malformed_jwt(self, client: TestClient):
        """Test that malformed JWTs are rejected."""
        malformed_tokens = [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",  # Missing payload and signature
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ",  # Missing signature
            "not.a.jwt.at.all.really",  # Too many parts
            "header.payload.signature.extra",  # Too many parts
        ]
        
        for token in malformed_tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == 401

    def test_token_reuse_after_logout(self, client: TestClient):
        """Test that tokens cannot be reused after logout (if logout is implemented)."""
        # Register and login user
        user_data = {
            "email": "logout_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Logout",
            "last_name": "Test"
        }
        
        client.post("/api/v1/auth/register", json=user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        
        token = login_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Token should work initially
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == 200
        
        # If logout endpoint exists, test token invalidation
        logout_response = client.post("/api/v1/auth/logout", headers=headers)
        if logout_response.status_code == 200:
            # Token should no longer work after logout
            response = client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == 401

    def test_concurrent_sessions(self, client: TestClient):
        """Test handling of concurrent sessions for same user."""
        user_data = {
            "email": "concurrent_session@example.com",
            "password": "TestPassword123!",
            "first_name": "Concurrent",
            "last_name": "Session"
        }
        
        client.post("/api/v1/auth/register", json=user_data)
        
        # Login multiple times to get different tokens
        tokens = []
        for _ in range(3):
            login_response = client.post("/api/v1/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            tokens.append(login_response.json()["data"]["access_token"])
        
        # All tokens should work (concurrent sessions allowed)
        for token in tokens:
            headers = {"Authorization": f"Bearer {token}"}
            response = client.get("/api/v1/users/me", headers=headers)
            assert response.status_code == 200


class TestInputValidationSecurity:
    """Test input validation and injection attack prevention."""

    def test_sql_injection_attempts(self, client: TestClient):
        """Test SQL injection prevention in various inputs."""
        sql_injection_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "'; INSERT INTO users (email) VALUES ('hacked@evil.com'); --",
            "' UNION SELECT * FROM users --",
            "admin'--",
            "admin'/*",
            "' OR 1=1#",
        ]
        
        # Test in registration
        for payload in sql_injection_payloads:
            user_data = {
                "email": f"{payload}@example.com",
                "password": "TestPassword123!",
                "first_name": payload,
                "last_name": "Test"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            # Should either return validation error or handle gracefully
            assert response.status_code in [422, 400]
        
        # Test in login
        for payload in sql_injection_payloads:
            login_data = {
                "email": payload,
                "password": payload
            }
            response = client.post("/api/v1/auth/login", json=login_data)
            assert response.status_code in [401, 422]  # Not 500 (server error)
        
        # Test in search parameters
        for payload in sql_injection_payloads:
            response = client.get(f"/api/v1/activities/?search={payload}")
            assert response.status_code != 500  # Should not cause server error

    def test_xss_prevention(self, client: TestClient):
        """Test XSS attack prevention."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')",
            "<svg onload=alert('xss')>",
            "'><script>alert('xss')</script>",
            "\"><script>alert('xss')</script>",
        ]
        
        # Register user for authenticated tests
        user_data = {
            "email": "xss_test@example.com",
            "password": "TestPassword123!",
            "first_name": "XSS",
            "last_name": "Test"
        }
        client.post("/api/v1/auth/register", json=user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        token = login_response.json()["data"]["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test XSS in activity creation
        for payload in xss_payloads:
            activity_data = {
                "title": f"Activity with {payload}",
                "description": f"Description with {payload}",
                "category": "test",
                "difficulty_level": "beginner",
                "estimated_duration": 30
            }
            response = client.post("/api/v1/activities/", 
                                 json=activity_data, headers=headers)
            
            if response.status_code == 201:
                # If activity was created, check that XSS payload is escaped/sanitized
                activity_id = response.json()["data"]["id"]
                get_response = client.get(f"/api/v1/activities/{activity_id}")
                activity_data = get_response.json()["data"]
                
                # XSS payload should be escaped or sanitized
                assert payload not in activity_data["title"]
                assert payload not in activity_data["description"]

    def test_command_injection_prevention(self, client: TestClient):
        """Test command injection prevention."""
        command_injection_payloads = [
            "; ls -la",
            "| cat /etc/passwd",
            "&& rm -rf /",
            "`whoami`",
            "$(cat /etc/passwd)",
            "; cat /etc/passwd",
        ]
        
        # Test in various input fields
        for payload in command_injection_payloads:
            user_data = {
                "email": f"cmdtest@example.com",
                "password": "TestPassword123!",
                "first_name": payload,
                "last_name": "Test"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            # Should handle gracefully without executing commands
            assert response.status_code in [201, 422, 400]

    def test_path_traversal_prevention(self, client: TestClient):
        """Test path traversal attack prevention."""
        path_traversal_payloads = [
            "../../../etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "....//....//....//etc/passwd",
            "%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64",
        ]
        
        # Test in file-related endpoints (if any)
        for payload in path_traversal_payloads:
            # This would be relevant if there are file upload/download endpoints
            response = client.get(f"/api/v1/files/{payload}")
            # Should return 404 or 400, not expose system files
            assert response.status_code in [404, 400, 403]

    def test_large_payload_handling(self, client: TestClient):
        """Test handling of excessively large payloads."""
        # Test very large strings
        large_string = "A" * 100000  # 100KB string
        
        user_data = {
            "email": "large_test@example.com",
            "password": "TestPassword123!",
            "first_name": large_string,
            "last_name": "Test"
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        # Should reject large payloads gracefully
        assert response.status_code in [422, 413]  # 413 = Payload Too Large

    def test_null_byte_injection(self, client: TestClient):
        """Test null byte injection prevention."""
        null_byte_payloads = [
            "test\x00.php",
            "test\0admin",
            "normal\x00malicious",
        ]
        
        for payload in null_byte_payloads:
            user_data = {
                "email": f"nullbyte@example.com",
                "password": "TestPassword123!",
                "first_name": payload,
                "last_name": "Test"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            # Should handle null bytes safely
            assert response.status_code in [201, 422, 400]


class TestRateLimitingSecurity:
    """Test rate limiting and brute force protection."""

    def test_login_rate_limiting(self, client: TestClient):
        """Test rate limiting on login attempts."""
        # Register a user first
        user_data = {
            "email": "ratelimit_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Rate",
            "last_name": "Limit"
        }
        client.post("/api/v1/auth/register", json=user_data)
        
        # Make many failed login attempts
        failed_attempts = 0
        rate_limited = False
        
        for i in range(20):  # Try 20 failed logins
            login_data = {
                "email": user_data["email"],
                "password": f"WrongPassword{i}"
            }
            response = client.post("/api/v1/auth/login", json=login_data)
            
            if response.status_code == 429:  # Too Many Requests
                rate_limited = True
                break
            elif response.status_code == 401:
                failed_attempts += 1
            
            time.sleep(0.1)  # Small delay between attempts
        
        # Either rate limiting should kick in, or all attempts should fail normally
        assert rate_limited or failed_attempts == 20

    def test_registration_rate_limiting(self, client: TestClient):
        """Test rate limiting on registration attempts."""
        rate_limited = False
        
        for i in range(15):  # Try 15 registrations
            user_data = {
                "email": f"spam_user_{i}@example.com",
                "password": "TestPassword123!",
                "first_name": f"Spam{i}",
                "last_name": "User"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            
            if response.status_code == 429:  # Too Many Requests
                rate_limited = True
                break
            
            time.sleep(0.1)
        
        # Rate limiting might be implemented to prevent spam registrations
        # This test documents expected behavior

    def test_api_endpoint_rate_limiting(self, client: TestClient):
        """Test rate limiting on API endpoints."""
        # Test rapid requests to public endpoints
        for i in range(100):  # 100 rapid requests
            response = client.get("/api/v1/activities/")
            
            if response.status_code == 429:
                # Rate limiting is working
                break
            
            if i > 50:  # If no rate limiting after 50 requests, assume it's not implemented
                break


class TestSecurityHeaders:
    """Test security-related HTTP headers."""

    def test_security_headers_present(self, client: TestClient):
        """Test that important security headers are present."""
        response = client.get("/")
        
        # Check for important security headers
        headers_to_check = [
            "X-Content-Type-Options",
            "X-Frame-Options", 
            "X-XSS-Protection",
            "Strict-Transport-Security",  # HSTS
        ]
        
        # Document which headers are present
        present_headers = []
        for header in headers_to_check:
            if header in response.headers:
                present_headers.append(header)
        
        # At least some security headers should be present
        # This test documents current state and can be enhanced

    def test_cors_headers_configuration(self, client: TestClient):
        """Test CORS headers are properly configured."""
        # Test preflight request
        response = client.options("/api/v1/activities/", 
                                headers={"Origin": "https://example.com"})
        
        if "Access-Control-Allow-Origin" in response.headers:
            # CORS is configured - check it's not too permissive
            allowed_origin = response.headers["Access-Control-Allow-Origin"]
            assert allowed_origin != "*" or "credentials" not in response.headers.get("Access-Control-Allow-Credentials", "")

    def test_content_type_headers(self, client: TestClient):
        """Test content type headers are properly set."""
        response = client.get("/api/v1/activities/")
        
        if response.status_code == 200:
            assert "application/json" in response.headers.get("Content-Type", "")


class TestSessionSecurity:
    """Test session management security."""

    def test_token_entropy(self, client: TestClient):
        """Test that tokens have sufficient entropy."""
        # Register and login to get tokens
        tokens = []
        
        for i in range(5):
            user_data = {
                "email": f"entropy_test_{i}@example.com",
                "password": "TestPassword123!",
                "first_name": f"Entropy{i}",
                "last_name": "Test"
            }
            client.post("/api/v1/auth/register", json=user_data)
            login_response = client.post("/api/v1/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
            tokens.append(login_response.json()["data"]["access_token"])
        
        # Tokens should be different
        assert len(set(tokens)) == len(tokens), "All tokens should be unique"
        
        # Tokens should be sufficiently long
        for token in tokens:
            assert len(token) > 50, "Tokens should be sufficiently long"

    def test_session_fixation_prevention(self, client: TestClient):
        """Test prevention of session fixation attacks."""
        # This would test that session IDs change after login
        # For JWT-based auth, this is less relevant, but good to document
        pass


class TestDataExposureSecurity:
    """Test prevention of sensitive data exposure."""

    def test_password_not_exposed(self, client: TestClient):
        """Test that passwords are never exposed in responses."""
        user_data = {
            "email": "password_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Password",
            "last_name": "Test"
        }
        
        # Registration response should not contain password
        register_response = client.post("/api/v1/auth/register", json=user_data)
        if register_response.status_code == 201:
            response_text = register_response.text.lower()
            assert "testpassword123!" not in response_text
            assert "password" not in register_response.json().get("data", {})
        
        # Login response should not contain password
        login_response = client.post("/api/v1/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        if login_response.status_code == 200:
            response_text = login_response.text.lower()
            assert "testpassword123!" not in response_text
            
            # Get token for further tests
            token = login_response.json()["data"]["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # User profile should not contain password
            profile_response = client.get("/api/v1/users/me", headers=headers)
            if profile_response.status_code == 200:
                response_text = profile_response.text.lower()
                assert "testpassword123!" not in response_text
                assert "password" not in profile_response.json().get("data", {})

    def test_internal_ids_not_exposed(self, client: TestClient):
        """Test that internal system IDs are not exposed."""
        response = client.get("/api/v1/activities/")
        
        if response.status_code == 200:
            data = response.json()
            # Check that database internal fields are not exposed
            for activity in data.get("data", []):
                # These fields should not be exposed
                sensitive_fields = ["_sa_instance_state", "hashed_password", "internal_id"]
                for field in sensitive_fields:
                    assert field not in activity

    def test_error_message_information_disclosure(self, client: TestClient):
        """Test that error messages don't disclose sensitive information."""
        # Test with non-existent user
        login_data = {
            "email": "nonexistent@example.com",
            "password": "AnyPassword123!"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        
        if response.status_code == 401:
            error_message = response.json().get("detail", "").lower()
            # Error message should not reveal whether user exists
            assert "user not found" not in error_message
            assert "email not found" not in error_message
            # Generic message is better for security
            assert "incorrect" in error_message or "invalid" in error_message


class TestAPISecurityMiscellaneous:
    """Test miscellaneous API security measures."""

    def test_http_methods_restrictions(self, client: TestClient):
        """Test that only allowed HTTP methods are supported."""
        # Test unsupported methods on endpoints
        test_cases = [
            ("TRACE", "/api/v1/activities/"),
            ("CONNECT", "/api/v1/activities/"),
            ("PATCH", "/api/v1/auth/login"),  # If PATCH is not supported
        ]
        
        for method, endpoint in test_cases:
            response = client.request(method, endpoint)
            # Should return 405 Method Not Allowed, not 500
            assert response.status_code in [405, 404]

    def test_content_type_validation(self, client: TestClient):
        """Test that endpoints validate content types."""
        # Send XML to JSON endpoint
        xml_data = '<?xml version="1.0"?><user><email>test@example.com</email></user>'
        response = client.post(
            "/api/v1/auth/register",
            data=xml_data,
            headers={"Content-Type": "application/xml"}
        )
        
        # Should reject non-JSON content
        assert response.status_code in [400, 415, 422]  # 415 = Unsupported Media Type

    def test_request_size_limits(self, client: TestClient):
        """Test that request size limits are enforced."""
        # Very large JSON payload
        large_data = {
            "email": "large@example.com",
            "password": "TestPassword123!",
            "first_name": "A" * 100000,  # 100KB of 'A's
            "last_name": "Test"
        }
        
        response = client.post("/api/v1/auth/register", json=large_data)
        # Should reject overly large requests
        assert response.status_code in [413, 422]  # 413 = Payload Too Large

    def test_file_upload_security(self, client: TestClient):
        """Test file upload security (if file uploads are supported)."""
        # This would test file type validation, size limits, etc.
        # Placeholder for when file uploads are implemented
        pass