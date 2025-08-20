"""
Test activity endpoints.
"""

import pytest
from httpx import AsyncClient
import sys
import os

# Add the app directory to the path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from models.models import User, Activity
from core.security import get_password_hash


@pytest.fixture
async def auth_user(db_session):
    """Create and return authenticated user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("TestPassword123"),
        first_name="Test",
        last_name="User",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
async def auth_headers(client: AsyncClient, auth_user):
    """Get authorization headers for authenticated user."""
    login_response = await client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123"
    })
    token = login_response.json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_activity(client: AsyncClient, auth_headers):
    """Test creating a new activity."""
    activity_data = {
        "title": "Apiculture pour débutants",
        "category": "agri",
        "summary": "Introduction à l'apiculture et gestion des ruches",
        "description": "Activité complète d'introduction à l'apiculture...",
        "duration_min": 180,
        "skill_tags": ["apiculture", "nature", "biologie"],
        "safety_level": 3,
        "materials": ["combinaison", "enfumoir", "gants"],
        "difficulty_level": 2,
        "min_participants": 1,
        "max_participants": 8,
        "location_type": "outdoor"
    }
    
    response = await client.post(
        "/api/v1/activities/",
        json=activity_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == activity_data["title"]
    assert data["data"]["category"] == activity_data["category"]


@pytest.mark.asyncio
async def test_list_activities(client: AsyncClient, db_session, auth_user):
    """Test listing activities."""
    # Create test activities
    activities = [
        Activity(
            title="Jardinage biologique",
            category="agri",
            summary="Techniques de jardinage biologique",
            duration_min=120,
            is_published=True,
            created_by=auth_user.id
        ),
        Activity(
            title="Cuisine traditionnelle",
            category="transfo",
            summary="Préparation de plats traditionnels",
            duration_min=90,
            is_published=True,
            created_by=auth_user.id
        )
    ]
    
    for activity in activities:
        db_session.add(activity)
    await db_session.commit()
    
    # Test listing
    response = await client.get("/api/v1/activities/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["items"]) == 2


@pytest.mark.asyncio
async def test_get_activity_by_id(client: AsyncClient, db_session, auth_user):
    """Test getting activity by ID."""
    activity = Activity(
        title="Poterie traditionnelle",
        category="artisanat", 
        summary="Création de poteries avec des techniques traditionnelles",
        duration_min=240,
        is_published=True,
        created_by=auth_user.id
    )
    db_session.add(activity)
    await db_session.commit()
    await db_session.refresh(activity)
    
    response = await client.get(f"/api/v1/activities/{activity.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == activity.title


@pytest.mark.asyncio 
async def test_update_activity(client: AsyncClient, db_session, auth_user, auth_headers):
    """Test updating an activity."""
    activity = Activity(
        title="Ancien titre",
        category="agri",
        summary="Ancienne description",
        duration_min=120,
        is_published=True,
        created_by=auth_user.id
    )
    db_session.add(activity)
    await db_session.commit()
    await db_session.refresh(activity)
    
    update_data = {
        "title": "Nouveau titre",
        "summary": "Nouvelle description"
    }
    
    response = await client.put(
        f"/api/v1/activities/{activity.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["title"] == "Nouveau titre"


@pytest.mark.asyncio
async def test_delete_activity(client: AsyncClient, db_session, auth_user, auth_headers):
    """Test deleting an activity."""
    activity = Activity(
        title="À supprimer",
        category="agri",
        summary="Cette activité sera supprimée",
        duration_min=60,
        is_published=True,
        created_by=auth_user.id
    )
    db_session.add(activity)
    await db_session.commit()
    await db_session.refresh(activity)
    
    response = await client.delete(
        f"/api/v1/activities/{activity.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True