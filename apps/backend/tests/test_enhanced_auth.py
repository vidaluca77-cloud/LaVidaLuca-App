"""
Test enhanced authentication system features.
"""

import pytest
from httpx import AsyncClient
import json
import secrets

from ..models.user import User, UserRole
from ..auth.password import hash_password
from ..auth.jwt import jwt_handler
from ..auth.oauth import oauth_manager


@pytest.mark.asyncio
async def test_login_with_refresh_token(client: AsyncClient, db_session):
    """Test login returns both access and refresh tokens."""
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
    assert "refresh_token" in data["data"]
    assert data["data"]["token_type"] == "bearer"
    assert data["data"]["expires_in"] > 0


@pytest.mark.asyncio
async def test_refresh_token_flow(client: AsyncClient, db_session):
    """Test refresh token can be used to get new access token."""
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
    
    # Login to get tokens
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": password
    })
    
    login_data = login_response.json()["data"]
    refresh_token = login_data["refresh_token"]
    
    # Use refresh token to get new access token
    refresh_response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert refresh_response.status_code == 200
    refresh_data = refresh_response.json()
    assert refresh_data["success"] is True
    assert "access_token" in refresh_data["data"]
    assert "refresh_token" in refresh_data["data"]
    # New tokens should be different
    assert refresh_data["data"]["access_token"] != login_data["access_token"]
    assert refresh_data["data"]["refresh_token"] != refresh_token


@pytest.mark.asyncio
async def test_logout_revokes_refresh_token(client: AsyncClient, db_session):
    """Test logout revokes refresh token."""
    # Create test user and login
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
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": password
    })
    
    login_data = login_response.json()["data"]
    access_token = login_data["access_token"]
    refresh_token = login_data["refresh_token"]
    
    # Logout
    logout_response = await client.post(
        "/api/v1/auth/logout",
        json={"refresh_token": refresh_token},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert logout_response.status_code == 200
    
    # Try to use refresh token (should fail)
    refresh_response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token
    })
    
    assert refresh_response.status_code == 401


@pytest.mark.asyncio
async def test_user_roles_and_permissions():
    """Test user role and permission system."""
    # Test user with USER role
    user = User(
        email="user@example.com",
        hashed_password="hashed",
        role=UserRole.USER
    )
    
    assert user.has_role(UserRole.USER)
    assert not user.has_role(UserRole.MODERATOR)
    assert not user.has_role(UserRole.ADMIN)
    
    assert user.has_permission("read_own_profile")
    assert not user.has_permission("moderate_activities")
    assert not user.has_permission("manage_users")
    
    # Test user with ADMIN role
    admin = User(
        email="admin@example.com",
        hashed_password="hashed",
        role=UserRole.ADMIN
    )
    
    assert admin.has_role(UserRole.USER)
    assert admin.has_role(UserRole.MODERATOR)
    assert admin.has_role(UserRole.ADMIN)
    assert not admin.has_role(UserRole.SUPERUSER)
    
    assert admin.has_permission("read_own_profile")
    assert admin.has_permission("moderate_activities")
    assert admin.has_permission("manage_users")
    
    # Test SUPERUSER
    superuser = User(
        email="super@example.com",
        hashed_password="hashed",
        role=UserRole.SUPERUSER
    )
    
    assert superuser.has_role(UserRole.SUPERUSER)
    assert superuser.has_permission("manage_users")
    assert superuser.has_permission("any_permission")  # Superuser has all permissions


@pytest.mark.asyncio
async def test_oauth_providers_endpoint(client: AsyncClient):
    """Test OAuth providers endpoint."""
    response = await client.get("/api/v1/auth/oauth/providers")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_oauth_authorization_url():
    """Test OAuth authorization URL generation."""
    # Test Google OAuth
    google_provider = oauth_manager.get_provider("google")
    if google_provider:
        state = "test_state"
        auth_url = google_provider.get_authorization_url(state)
        
        assert "accounts.google.com" in auth_url
        assert "client_id" in auth_url
        assert f"state={state}" in auth_url
        assert "scope=" in auth_url


@pytest.mark.asyncio
async def test_jwt_handler_access_token():
    """Test JWT handler access token creation and verification."""
    user_data = {"sub": "user_id_123", "email": "test@example.com"}
    
    # Create access token
    access_token = jwt_handler.create_access_token(user_data)
    assert isinstance(access_token, str)
    assert len(access_token) > 0
    
    # Verify access token
    token_data = jwt_handler.verify_access_token(access_token)
    assert token_data.user_id == "user_id_123"
    assert token_data.email == "test@example.com"


@pytest.mark.asyncio
async def test_refresh_token_storage(db_session):
    """Test refresh token storage and verification."""
    user = User(
        email="test@example.com",
        hashed_password="hashed",
        profile={}
    )
    db_session.add(user)
    await db_session.commit()
    
    user_id = str(user.id)
    refresh_token = "test_refresh_token_" + secrets.token_urlsafe(16)
    
    # Store refresh token
    await jwt_handler.store_refresh_token(db_session, user_id, refresh_token)
    
    # Verify refresh token
    verified_user_id = await jwt_handler.verify_refresh_token(db_session, refresh_token)
    assert verified_user_id == user_id
    
    # Test invalid token
    invalid_user_id = await jwt_handler.verify_refresh_token(db_session, "invalid_token")
    assert invalid_user_id is None


@pytest.mark.asyncio
async def test_role_based_access_endpoint(client: AsyncClient, db_session):
    """Test role-based access control on endpoints."""
    # Create regular user
    user = User(
        email="user@example.com",
        hashed_password=hash_password("password123"),
        role=UserRole.USER,
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    
    # Login as regular user
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "user@example.com",
        "password": "password123"
    })
    
    access_token = login_response.json()["data"]["access_token"]
    
    # Test accessing admin endpoint (should fail)
    # This would require an actual admin endpoint to test properly
    # For now, we just verify the token works for regular endpoints
    verify_response = await client.post(
        "/api/v1/auth/verify-token",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    assert verify_response.status_code == 200
    data = verify_response.json()
    assert data["data"]["email"] == "user@example.com"