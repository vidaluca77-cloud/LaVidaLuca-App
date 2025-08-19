"""
Test authentication endpoints.
"""

import pytest
from httpx import AsyncClient

from ..models.user import User
from ..auth.password import hash_password


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == user_data["email"]
    assert data["data"]["first_name"] == user_data["first_name"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db_session):
    """Test registration with duplicate email."""
    # Create existing user
    existing_user = User(
        email="test@example.com",
        hashed_password=hash_password("password123"),
        first_name="Existing",
        last_name="User"
    )
    db_session.add(existing_user)
    await db_session.commit()
    
    # Try to register with same email
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient, db_session):
    """Test user login."""
    # Create test user
    password = "TestPassword123"
    user = User(
        email="test@example.com",
        hashed_password=hash_password(password),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    login_data = {
        "email": "test@example.com",
        "password": password
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    
    assert response.status_code == 401
    data = response.json()
    assert data["success"] is False


@pytest.mark.asyncio
async def test_verify_token(client: AsyncClient, db_session):
    """Test token verification."""
    # Create and login user first
    password = "TestPassword123"
    user = User(
        email="test@example.com",
        hashed_password=hash_password(password),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login to get token
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": password
    })
    token = login_response.json()["data"]["access_token"]
    
    # Verify token
    response = await client.post(
        "/api/v1/auth/verify-token",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["email"] == "test@example.com"