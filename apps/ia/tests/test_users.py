import pytest
from fastapi.testclient import TestClient


def test_get_current_user(client: TestClient, auth_headers, test_user):
    """Test getting current user profile."""
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_update_current_user(client: TestClient, auth_headers, test_user):
    """Test updating current user profile."""
    response = client.put(
        "/users/me",
        headers=auth_headers,
        json={
            "full_name": "Updated Name",
            "location": "New Location",
            "skills": ["new_skill"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["location"] == "New Location"
    assert "new_skill" in data["skills"]


def test_get_user_without_auth(client: TestClient):
    """Test getting user profile without authentication."""
    response = client.get("/users/me")
    assert response.status_code == 403  # Should be forbidden without auth