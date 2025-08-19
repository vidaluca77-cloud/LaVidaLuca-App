"""
Test profile endpoints.
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..models.profile import Profile
from ..auth.password import hash_password


@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient, db_session: AsyncSession):
    """Test profile creation."""
    # Create a user first
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    # Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    
    # Create profile
    profile_data = {
        "skills": ["agriculture", "menuiserie"],
        "location": "Bretagne",
        "interests": ["permaculture", "construction"],
        "experience_level": "intermediate",
        "collaboration_preference": "team"
    }
    
    response = await client.post(
        "/api/v1/profiles/",
        json=profile_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["skills"] == profile_data["skills"]
    assert data["data"]["location"] == profile_data["location"]
    assert data["data"]["user_id"] == str(user.id)


@pytest.mark.asyncio
async def test_get_my_profile(client: AsyncClient, db_session: AsyncSession):
    """Test getting current user's profile."""
    # Create user and profile
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    profile = Profile(
        user_id=user.id,
        skills=["agriculture"],
        location="Bretagne",
        interests=["permaculture"]
    )
    db_session.add(profile)
    await db_session.commit()
    
    # Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    token = login_response.json()["data"]["access_token"]
    
    # Get profile
    response = await client.get(
        "/api/v1/profiles/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["skills"] == ["agriculture"]
    assert data["data"]["location"] == "Bretagne"


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, db_session: AsyncSession):
    """Test profile update."""
    # Create user and profile
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    profile = Profile(
        user_id=user.id,
        skills=["agriculture"],
        location="Bretagne"
    )
    db_session.add(profile)
    await db_session.commit()
    
    # Login to get token
    login_response = await client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "TestPassword123"}
    )
    token = login_response.json()["data"]["access_token"]
    
    # Update profile
    update_data = {
        "skills": ["agriculture", "menuiserie", "cuisine"],
        "experience_level": "advanced",
        "interests": ["permaculture", "construction", "energie"]
    }
    
    response = await client.put(
        "/api/v1/profiles/me",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["skills"]) == 3
    assert data["data"]["experience_level"] == "advanced"
    assert data["data"]["is_complete"] is True  # Should be marked complete now


@pytest.mark.asyncio
async def test_list_public_profiles(client: AsyncClient, db_session: AsyncSession):
    """Test listing public profiles."""
    # Create multiple users with profiles
    for i in range(3):
        user = User(
            email=f"test{i}@example.com",
            hashed_password=hash_password("TestPassword123"),
            first_name=f"Test{i}",
            last_name="User"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        profile = Profile(
            user_id=user.id,
            skills=[f"skill{i}"],
            location=f"Location{i}",
            interests=[f"interest{i}"],
            is_public=True
        )
        db_session.add(profile)
    
    await db_session.commit()
    
    # List profiles
    response = await client.get("/api/v1/profiles/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["total"] == 3
    assert len(data["data"]["items"]) == 3


@pytest.mark.asyncio
async def test_profile_search_filters(client: AsyncClient, db_session: AsyncSession):
    """Test profile search with filters."""
    # Create user with specific profile
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        first_name="Test",
        last_name="User"
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    profile = Profile(
        user_id=user.id,
        skills=["agriculture", "menuiserie"],
        location="Bretagne",
        interests=["permaculture"],
        experience_level="intermediate",
        is_public=True
    )
    db_session.add(profile)
    await db_session.commit()
    
    # Search by skills
    response = await client.get("/api/v1/profiles/?skills=agriculture")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1
    
    # Search by location
    response = await client.get("/api/v1/profiles/?location=Bretagne")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1
    
    # Search by experience level
    response = await client.get("/api/v1/profiles/?experience_level=intermediate")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["total"] == 1


@pytest.mark.asyncio
async def test_get_available_skills(client: AsyncClient, db_session: AsyncSession):
    """Test getting available skills from profiles."""
    # Create users with different skills
    skills_sets = [
        ["agriculture", "menuiserie"],
        ["cuisine", "agriculture"], 
        ["menuiserie", "electricite"]
    ]
    
    for i, skills in enumerate(skills_sets):
        user = User(
            email=f"test{i}@example.com",
            hashed_password=hash_password("TestPassword123"),
            first_name=f"Test{i}",
            last_name="User"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        profile = Profile(
            user_id=user.id,
            skills=skills,
            is_public=True
        )
        db_session.add(profile)
    
    await db_session.commit()
    
    # Get available skills
    response = await client.get("/api/v1/profiles/search/skills")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    
    available_skills = data["data"]
    expected_skills = {"agriculture", "menuiserie", "cuisine", "electricite"}
    assert set(available_skills) == expected_skills