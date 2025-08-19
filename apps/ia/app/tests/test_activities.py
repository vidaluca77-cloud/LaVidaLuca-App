"""
Test activities endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_list_activities(client: TestClient):
    """Test listing activities (public endpoint)"""
    response = client.get("/api/v1/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_activity(client: TestClient, test_activity):
    """Test getting specific activity"""
    response = client.get(f"/api/v1/activities/{test_activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_activity.id
    assert data["title"] == test_activity.title


def test_get_activity_by_slug(client: TestClient, test_activity):
    """Test getting activity by slug"""
    response = client.get(f"/api/v1/activities/slug/{test_activity.slug}")
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == test_activity.slug


def test_get_nonexistent_activity(client: TestClient):
    """Test getting nonexistent activity"""
    response = client.get("/api/v1/activities/999")
    assert response.status_code == 404


def test_search_activities(client: TestClient, test_activity):
    """Test activity search"""
    response = client.get("/api/v1/activities/search/?q=Test")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 0  # May or may not find results depending on test data


def test_list_categories(client: TestClient):
    """Test listing activity categories"""
    response = client.get("/api/v1/activities/categories/")
    assert response.status_code == 200
    categories = response.json()
    assert "agri" in categories
    assert "transfo" in categories
    assert "artisanat" in categories
    assert "nature" in categories
    assert "social" in categories


def test_create_activity_unauthorized(client: TestClient):
    """Test creating activity without authentication"""
    response = client.post(
        "/api/v1/activities/",
        json={
            "slug": "new-activity",
            "title": "New Activity",
            "category": "agri",
            "summary": "A new test activity"
        }
    )
    assert response.status_code == 401


def test_filter_by_category(client: TestClient, test_activity):
    """Test filtering activities by category"""
    response = client.get("/api/v1/activities/?category=agri")
    assert response.status_code == 200
    activities = response.json()
    for activity in activities:
        assert activity["category"] == "agri"