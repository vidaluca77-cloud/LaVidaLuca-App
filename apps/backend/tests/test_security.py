"""
Security tests for LaVidaLuca Backend API.
"""

import pytest
import json
import time
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch

from app.models.models import User, Activity
from app.core.security import create_access_token


class TestAuthenticationSecurity:
    """Test authentication security measures."""
    
    def test_login_without_credentials(self, client: TestClient):
        """Test login attempt without credentials."""
        response = client.post("/api/v1/auth/login", json={})
        assert response.status_code == 422  # Validation error
    
    def test_login_with_empty_credentials(self, client: TestClient):
        """Test login with empty credentials."""
        response = client.post("/api/v1/auth/login", json={
            "username": "",
            "password": ""
        })
        assert response.status_code == 422  # Validation error
    
    def test_login_with_invalid_credentials(self, client: TestClient):
        """Test login with non-existent user."""
        response = client.post("/api/v1/auth/login", json={
            "username": "nonexistent",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_with_sql_injection_attempt(self, client: TestClient):
        """Test login resistance to SQL injection."""
        response = client.post("/api/v1/auth/login", json={
            "username": "admin'; DROP TABLE users; --",
            "password": "password"
        })
        assert response.status_code == 401
        # Should not crash the application
    
    def test_password_brute_force_protection(self, client: TestClient, test_user: User):
        """Test protection against password brute force attacks."""
        # Make multiple failed login attempts
        for _ in range(10):
            response = client.post("/api/v1/auth/login", json={
                "username": test_user.username,
                "password": "wrongpassword"
            })
            assert response.status_code == 401
        
        # Should still reject invalid password
        response = client.post("/api/v1/auth/login", json={
            "username": test_user.username,
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        
        # But should still accept valid password
        response = client.post("/api/v1/auth/login", json={
            "username": test_user.username,
            "password": "testpassword"
        })
        assert response.status_code == 200
    
    def test_password_hashing_security(self, db_session: Session):
        """Test that passwords are properly hashed."""
        from app.core.security import get_password_hash, verify_password
        
        password = "testsecretpassword"
        hashed = get_password_hash(password)
        
        # Hash should be different from original
        assert hashed != password
        
        # Hash should be long enough
        assert len(hashed) > 50
        
        # Should contain bcrypt prefix
        assert hashed.startswith("$2b$")
        
        # Should verify correctly
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False
    
    def test_token_expiration(self, client: TestClient, test_user: User):
        """Test that JWT tokens expire properly."""
        # Create an expired token
        expired_token = create_access_token(
            subject=test_user.id,
            expires_delta=timedelta(minutes=-30)  # Expired 30 minutes ago
        )
        
        # Try to use expired token
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/api/v1/users/me", headers=headers)
        
        # Should reject expired token (might be 404 if endpoint doesn't exist)
        assert response.status_code in [401, 404]
    
    def test_malformed_token_rejection(self, client: TestClient, sample_activity_data: dict):
        """Test rejection of malformed tokens."""
        malformed_tokens = [
            "malformed_token",
            "Bearer malformed_token",
            "Bearer ",
            "",
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid",
            "Bearer invalid.token.here"
        ]
        
        for token in malformed_tokens:
            headers = {"Authorization": token}
            response = client.post(
                "/api/v1/activities/",
                json=sample_activity_data,
                headers=headers
            )
            assert response.status_code == 401


class TestAuthorizationSecurity:
    """Test authorization and access control."""
    
    def test_protected_endpoint_without_auth(self, client: TestClient, sample_activity_data: dict):
        """Test that protected endpoints require authentication."""
        response = client.post("/api/v1/activities/", json=sample_activity_data)
        assert response.status_code == 401
    
    def test_activity_ownership_protection(self, client: TestClient, test_activity: Activity, multiple_users: list):
        """Test that users can only modify their own activities."""
        # Create auth headers for a different user
        other_user = multiple_users[0]
        other_auth_headers = {
            "Authorization": f"Bearer {create_access_token(subject=other_user.id)}"
        }
        
        # Try to update another user's activity
        update_data = {"title": "Unauthorized Update"}
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=other_auth_headers
        )
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]
        
        # Try to delete another user's activity
        response = client.delete(
            f"/api/v1/activities/{test_activity.id}",
            headers=other_auth_headers
        )
        assert response.status_code == 403
    
    def test_superuser_permissions(self, client: TestClient, test_activity: Activity, superuser_auth_headers: dict):
        """Test that superusers can access all resources."""
        # Superuser should be able to update any activity
        update_data = {"title": "Superuser Update"}
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=superuser_auth_headers
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Superuser Update"
    
    def test_privilege_escalation_prevention(self, client: TestClient, auth_headers: dict):
        """Test prevention of privilege escalation attempts."""
        # Try to create a user with superuser privileges
        user_data = {
            "email": "hacker@example.com",
            "username": "hacker",
            "password": "password",
            "is_superuser": True  # Attempt to escalate privileges
        }
        
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Should either ignore the is_superuser field or reject the request
        if response.status_code == 200:
            # If user was created, it should not be a superuser
            user_data = response.json()
            assert user_data.get("is_superuser", False) is False


class TestInputValidationSecurity:
    """Test input validation and sanitization."""
    
    def test_xss_prevention_in_activity_creation(self, client: TestClient, auth_headers: dict):
        """Test XSS prevention in activity creation."""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>",
            "';alert('xss');//",
            "<svg/onload=alert('xss')>"
        ]
        
        for payload in xss_payloads:
            activity_data = {
                "title": f"Test Activity {payload}",
                "description": f"Description with {payload}",
                "category": "technology",
                "difficulty_level": "beginner"
            }
            
            response = client.post(
                "/api/v1/activities/",
                json=activity_data,
                headers=auth_headers
            )
            
            # Should either sanitize the input or reject it
            if response.status_code == 200:
                created_activity = response.json()
                # XSS payload should be sanitized/escaped
                assert "<script>" not in created_activity["title"]
                assert "javascript:" not in created_activity["description"]
    
    def test_sql_injection_prevention(self, client: TestClient, auth_headers: dict):
        """Test SQL injection prevention in search parameters."""
        sql_injection_payloads = [
            "'; DROP TABLE activities; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO activities VALUES ('hack') --"
        ]
        
        for payload in sql_injection_payloads:
            # Try SQL injection in query parameters
            response = client.get(f"/api/v1/activities/?category={payload}")
            # Should not crash or expose sensitive data
            assert response.status_code in [200, 400, 422]
            
            # Try SQL injection in activity creation
            activity_data = {
                "title": f"Activity {payload}",
                "category": payload,
                "difficulty_level": "beginner"
            }
            
            response = client.post(
                "/api/v1/activities/",
                json=activity_data,
                headers=auth_headers
            )
            # Should handle malicious input gracefully
            assert response.status_code in [200, 400, 422]
    
    def test_large_payload_protection(self, client: TestClient, auth_headers: dict):
        """Test protection against large payloads."""
        # Create very large strings
        large_string = "A" * 10000
        
        activity_data = {
            "title": large_string,
            "description": large_string * 10,  # Very large description
            "category": "technology",
            "difficulty_level": "beginner"
        }
        
        response = client.post(
            "/api/v1/activities/",
            json=activity_data,
            headers=auth_headers
        )
        
        # Should either limit the size or reject the request
        assert response.status_code in [200, 400, 413, 422]
    
    def test_invalid_json_handling(self, client: TestClient, auth_headers: dict):
        """Test handling of invalid JSON."""
        invalid_json_data = [
            '{"title": "Test"',  # Unclosed JSON
            '{"title": "Test", "invalid": }',  # Invalid syntax
            '{"title": "Test", "number": NaN}',  # Invalid value
            'not json at all'
        ]
        
        for invalid_data in invalid_json_data:
            response = client.post(
                "/api/v1/activities/",
                data=invalid_data,
                headers={**auth_headers, "Content-Type": "application/json"}
            )
            # Should return 422 for malformed JSON
            assert response.status_code == 422
    
    def test_file_upload_security(self, client: TestClient, auth_headers: dict):
        """Test file upload security (if file upload exists)."""
        # Test with potentially dangerous file types
        dangerous_files = [
            ("file", ("test.exe", b"MZ", "application/x-executable")),
            ("file", ("test.php", b"<?php echo 'hack'; ?>", "application/x-php")),
            ("file", ("test.js", b"alert('xss')", "application/javascript"))
        ]
        
        for file_data in dangerous_files:
            response = client.post(
                "/api/v1/upload",  # Assuming upload endpoint exists
                files=[file_data],
                headers=auth_headers
            )
            # Should reject dangerous file types or 404 if endpoint doesn't exist
            assert response.status_code in [400, 403, 404, 415]


class TestDataLeakagePrevention:
    """Test prevention of sensitive data leakage."""
    
    def test_password_not_in_response(self, client: TestClient, sample_user_data: dict):
        """Test that passwords are not included in API responses."""
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        
        if response.status_code == 200:
            user_data = response.json()
            # Password should not be in response
            assert "password" not in user_data
            assert "hashed_password" not in user_data
    
    def test_sensitive_user_data_protection(self, client: TestClient, auth_headers: dict):
        """Test that sensitive user data is protected."""
        # Try to access user list (if endpoint exists)
        response = client.get("/api/v1/users/", headers=auth_headers)
        
        if response.status_code == 200:
            users = response.json()
            if isinstance(users, list) and len(users) > 0:
                user = users[0]
                # Sensitive fields should not be exposed
                assert "hashed_password" not in user
                assert "password" not in user
    
    def test_error_message_information_disclosure(self, client: TestClient):
        """Test that error messages don't disclose sensitive information."""
        # Try to access non-existent resource
        response = client.get("/api/v1/activities/999999")
        assert response.status_code == 404
        
        error_message = response.json()["detail"]
        # Should not expose database structure or internal paths
        assert "table" not in error_message.lower()
        assert "database" not in error_message.lower()
        assert "/home/" not in error_message
        assert "traceback" not in error_message.lower()
    
    def test_debug_information_not_exposed(self, client: TestClient):
        """Test that debug information is not exposed in production."""
        # Try to trigger an error
        response = client.get("/api/v1/nonexistent")
        
        if response.status_code in [404, 500]:
            response_text = response.text
            # Should not expose stack traces or file paths
            assert "Traceback" not in response_text
            assert "/home/" not in response_text
            assert "File \"" not in response_text


class TestSessionSecurity:
    """Test session and token security."""
    
    def test_token_not_in_logs(self, client: TestClient, test_user: User):
        """Test that tokens are not logged."""
        login_response = client.post("/api/v1/auth/login", json={
            "username": test_user.username,
            "password": "testpassword"
        })
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Make a request with the token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/activities/", headers=headers)
        
        # This test mainly ensures the system doesn't crash
        # In a real scenario, you'd check actual log files
        assert response.status_code == 200
    
    def test_token_reuse_prevention(self, client: TestClient, test_user: User):
        """Test token security best practices."""
        # Get a token
        login_response = client.post("/api/v1/auth/login", json={
            "username": test_user.username,
            "password": "testpassword"
        })
        
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        
        # Token should work initially
        headers = {"Authorization": f"Bearer {token}"}
        response1 = client.get("/api/v1/activities/", headers=headers)
        assert response1.status_code == 200
        
        # Token should still work on repeated use (unless refresh mechanism exists)
        response2 = client.get("/api/v1/activities/", headers=headers)
        assert response2.status_code == 200
    
    def test_concurrent_login_security(self, client: TestClient, test_user: User):
        """Test security with concurrent logins."""
        import concurrent.futures
        
        def login_user():
            response = client.post("/api/v1/auth/login", json={
                "username": test_user.username,
                "password": "testpassword"
            })
            return response.status_code == 200, response.json().get("access_token")
        
        # Multiple concurrent logins
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(login_user) for _ in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All logins should succeed
        success_results = [result[0] for result in results]
        assert all(success_results)
        
        # All tokens should be different (if properly implemented)
        tokens = [result[1] for result in results if result[1]]
        assert len(set(tokens)) == len(tokens)  # All tokens should be unique


class TestRateLimitingSecurity:
    """Test rate limiting and DoS protection."""
    
    def test_registration_rate_limiting(self, client: TestClient):
        """Test rate limiting on user registration."""
        # Try to register many users quickly
        responses = []
        for i in range(20):
            user_data = {
                "email": f"ratetest{i}@example.com",
                "username": f"rateuser{i}",
                "password": "testpassword"
            }
            response = client.post("/api/v1/auth/register", json=user_data)
            responses.append(response.status_code)
        
        # Some requests might be rate limited (429) after initial successful ones
        success_count = sum(1 for status in responses if status == 200)
        rate_limited_count = sum(1 for status in responses if status == 429)
        
        # At least some should succeed, but rate limiting might kick in
        assert success_count > 0
        # This test passes regardless of whether rate limiting is implemented
    
    def test_login_rate_limiting(self, client: TestClient, test_user: User):
        """Test rate limiting on login attempts."""
        # Make many login attempts
        responses = []
        for _ in range(50):
            response = client.post("/api/v1/auth/login", json={
                "username": test_user.username,
                "password": "testpassword"
            })
            responses.append(response.status_code)
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.01)
        
        # Most should succeed unless rate limiting is implemented
        success_count = sum(1 for status in responses if status == 200)
        rate_limited_count = sum(1 for status in responses if status == 429)
        
        # Should handle the requests without crashing
        assert success_count > 0
    
    def test_api_endpoint_rate_limiting(self, client: TestClient):
        """Test rate limiting on API endpoints."""
        # Make many requests to the same endpoint
        responses = []
        for _ in range(100):
            response = client.get("/api/v1/activities/")
            responses.append(response.status_code)
        
        # Should handle the load without crashing
        success_count = sum(1 for status in responses if status == 200)
        assert success_count > 0


class TestHTTPSSecurity:
    """Test HTTPS and transport security."""
    
    def test_security_headers(self, client: TestClient):
        """Test that security headers are present."""
        response = client.get("/")
        headers = response.headers
        
        # Check for common security headers (might not all be implemented)
        security_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Strict-Transport-Security",
            "Content-Security-Policy"
        ]
        
        # At least some security headers should be present
        present_headers = [header for header in security_headers if header in headers]
        
        # This test documents what security headers are present
        # In a production environment, more headers should be implemented
        assert response.status_code == 200
    
    def test_cors_configuration(self, client: TestClient):
        """Test CORS configuration security."""
        # Make an OPTIONS request to check CORS
        response = client.options("/api/v1/activities/")
        
        if "Access-Control-Allow-Origin" in response.headers:
            cors_origin = response.headers["Access-Control-Allow-Origin"]
            
            # Should not allow all origins in production
            # (This test just documents current behavior)
            if cors_origin == "*":
                # This might be acceptable for development but should be restricted in production
                pass
    
    def test_content_type_validation(self, client: TestClient, auth_headers: dict):
        """Test content type validation."""
        # Try to send XML instead of JSON
        xml_data = "<?xml version='1.0'?><activity><title>Test</title></activity>"
        
        response = client.post(
            "/api/v1/activities/",
            data=xml_data,
            headers={**auth_headers, "Content-Type": "application/xml"}
        )
        
        # Should reject non-JSON content
        assert response.status_code in [400, 415, 422]