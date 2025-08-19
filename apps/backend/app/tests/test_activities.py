import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User, Activity
from app.core.security import get_password_hash, create_access_token


@pytest.fixture
def authenticated_user(db_session: Session):
    password = "testpassword"
    hashed_password = get_password_hash(password)
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password,
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(authenticated_user):
    token = create_access_token(subject=authenticated_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_activity(db_session: Session, authenticated_user):
    activity = Activity(
        title="Test Activity",
        description="A test activity for farming",
        category="Agriculture",
        difficulty_level="beginner",
        duration_minutes=60,
        location="Farm Field",
        equipment_needed="Basic tools",
        learning_objectives="Learn basic farming",
        is_published=True,
        creator_id=authenticated_user.id
    )
    db_session.add(activity)
    db_session.commit()
    db_session.refresh(activity)
    return activity


def test_get_activities(client: TestClient, sample_activity):
    response = client.get("/api/v1/activities/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Activity"


def test_get_activity_by_id(client: TestClient, sample_activity):
    response = client.get(f"/api/v1/activities/{sample_activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_activity.title
    assert data["id"] == sample_activity.id


def test_get_activity_not_found(client: TestClient):
    response = client.get("/api/v1/activities/999")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_create_activity(client: TestClient, auth_headers):
    activity_data = {
        "title": "New Activity",
        "description": "A new test activity",
        "category": "Livestock",
        "difficulty_level": "intermediate",
        "duration_minutes": 90,
        "location": "Barn",
        "equipment_needed": "Feed, water",
        "learning_objectives": "Learn animal care",
        "is_published": True
    }
    response = client.post("/api/v1/activities/", json=activity_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == activity_data["title"]
    assert data["category"] == activity_data["category"]


def test_create_activity_unauthorized(client: TestClient):
    activity_data = {
        "title": "Unauthorized Activity",
        "category": "Test"
    }
    response = client.post("/api/v1/activities/", json=activity_data)
    assert response.status_code == 401


def test_update_activity(client: TestClient, sample_activity, auth_headers):
    update_data = {
        "title": "Updated Activity Title",
        "description": "Updated description"
    }
    response = client.put(
        f"/api/v1/activities/{sample_activity.id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]


def test_update_activity_not_owner(client: TestClient, sample_activity, db_session):
    # Create another user
    other_user = User(
        email="other@example.com",
        username="otheruser",
        hashed_password=get_password_hash("password")
    )
    db_session.add(other_user)
    db_session.commit()
    
    # Get token for other user
    token = create_access_token(subject=other_user.id)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"title": "Unauthorized Update"}
    response = client.put(
        f"/api/v1/activities/{sample_activity.id}",
        json=update_data,
        headers=headers
    )
    assert response.status_code == 403


def test_delete_activity(client: TestClient, sample_activity, auth_headers):
    response = client.delete(f"/api/v1/activities/{sample_activity.id}", headers=auth_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.json()["message"]
    
    # Verify activity is deleted
    response = client.get(f"/api/v1/activities/{sample_activity.id}")
    assert response.status_code == 404


def test_get_activity_categories(client: TestClient, sample_activity):
    response = client.get("/api/v1/activities/categories/")
    assert response.status_code == 200
    data = response.json()
    assert "Agriculture" in data


def test_filter_activities_by_category(client: TestClient, sample_activity):
    response = client.get("/api/v1/activities/?category=Agriculture")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(activity["category"] == "Agriculture" for activity in data)


def test_filter_activities_by_difficulty(client: TestClient, sample_activity):
    response = client.get("/api/v1/activities/?difficulty=beginner")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(activity["difficulty_level"] == "beginner" for activity in data)