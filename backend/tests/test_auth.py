"""
Tests for authentication endpoints.
"""

import pytest
from httpx import AsyncClient


class TestAuth:
    """Test authentication endpoints."""
    
    async def test_register_new_user(self, client: AsyncClient, sample_user_data):
        """Test user registration."""
        response = await client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "user_id" in data["data"]
        assert data["message"] == "User registered successfully"
    
    async def test_register_duplicate_email(self, client: AsyncClient, test_user, sample_user_data):
        """Test registration with duplicate email."""
        sample_user_data["email"] = test_user.email
        
        response = await client.post("/api/auth/register", json=sample_user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Email already registered" in data["detail"]
    
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login."""
        login_data = {
            "email": test_user.email,
            "password": "testpassword"
        }
        
        response = await client.post("/api/auth/login-json", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    async def test_login_invalid_credentials(self, client: AsyncClient, test_user):
        """Test login with invalid credentials."""
        login_data = {
            "email": test_user.email,
            "password": "wrongpassword"
        }
        
        response = await client.post("/api/auth/login-json", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "Incorrect email or password" in data["detail"]
    
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with nonexistent user."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password"
        }
        
        response = await client.post("/api/auth/login-json", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert "Incorrect email or password" in data["detail"]
    
    async def test_get_current_user(self, client: AsyncClient, test_user, auth_headers):
        """Test getting current user info."""
        response = await client.get("/api/auth/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name
        assert data["last_name"] == test_user.last_name
    
    async def test_get_current_user_unauthorized(self, client: AsyncClient):
        """Test getting current user without authentication."""
        response = await client.get("/api/auth/me")
        
        assert response.status_code == 403  # HTTPBearer returns 403 for missing token
    
    async def test_get_current_user_invalid_token(self, client: AsyncClient):
        """Test getting current user with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = await client.get("/api/auth/me", headers=headers)
        
        assert response.status_code == 401
    
    async def test_refresh_token(self, client: AsyncClient, auth_headers):
        """Test token refresh."""
        response = await client.post("/api/auth/refresh", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    async def test_oauth_login_form(self, client: AsyncClient, test_user):
        """Test OAuth2 form-based login."""
        login_data = {
            "username": test_user.email,  # OAuth2 uses 'username' field
            "password": "testpassword"
        }
        
        response = await client.post("/api/auth/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"