import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.core.security import get_password_hash


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert data["is_active"] is True
    assert data["is_verified"] is False


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient, db_session: AsyncSession):
    """Test registration with duplicate email"""
    # Create a user first
    existing_user = User(
        email="existing@example.com",
        hashed_password=get_password_hash("password"),
        full_name="Existing User",
        is_active=True
    )
    db_session.add(existing_user)
    await db_session.commit()
    
    # Try to register with same email
    user_data = {
        "email": "existing@example.com",
        "password": "newpassword123",
        "full_name": "New User"
    }
    
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession):
    """Test successful login"""
    # Create a user
    user = User(
        email="login@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Login User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login
    login_data = {
        "email": "login@example.com",
        "password": "testpassword"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    
    response = await client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]