import pytest
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient, test_activity):
    """Test getting list of activities."""
    response = client.get("/activities/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Activity"


def test_get_activity_by_id(client: TestClient, test_activity):
    """Test getting activity by ID."""
    response = client.get(f"/activities/{test_activity.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Activity"
    assert data["category"] == "agri"


def test_get_activity_by_slug(client: TestClient, test_activity):
    """Test getting activity by slug."""
    response = client.get("/activities/slug/test-activity")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Activity"


def test_get_nonexistent_activity(client: TestClient):
    """Test getting non-existent activity."""
    response = client.get("/activities/99999")
    assert response.status_code == 404


def test_filter_activities_by_category(client: TestClient, test_activity):
    """Test filtering activities by category."""
    response = client.get("/activities/?category=agri")
    assert response.status_code == 200
    data = response.json()
    assert all(activity["category"] == "agri" for activity in data)