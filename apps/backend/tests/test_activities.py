"""
Test activity endpoints.
"""
import pytest
from fastapi.testclient import TestClient


def test_list_activities_empty(client: TestClient):
    """Test listing activities when none exist."""
    response = client.get("/api/v1/activities/")
    
    assert response.status_code == 200
    assert response.json() == []


def test_create_activity_requires_auth(client: TestClient, sample_activity_data):
    """Test that creating activity requires authentication."""
    response = client.post("/api/v1/activities/", json=sample_activity_data)
    
    assert response.status_code == 401


def test_list_activities_with_filter(client: TestClient):
    """Test listing activities with category filter."""
    response = client.get("/api/v1/activities/?category=agri")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_nonexistent_activity(client: TestClient):
    """Test getting non-existent activity returns 404."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/activities/{fake_uuid}")
    
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_activity_suggestions_requires_auth(client: TestClient):
    """Test that activity suggestions require authentication."""
    response = client.get("/api/v1/activities/suggestions")
    
    assert response.status_code == 401


def test_activity_suggestions_with_auth(client: TestClient, auth_headers):
    """Test getting activity suggestions with authentication."""
    response = client.get("/api/v1/activities/suggestions", headers=auth_headers)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_contact_form_submission(client: TestClient):
    """Test contact form submission."""
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "This is a test message",
        "activity_interest": "gardening"
    }
    
    response = client.post("/api/v1/contact/", json=contact_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "submitted successfully" in data["message"]


def test_contact_form_invalid_data(client: TestClient):
    """Test contact form with invalid data fails."""
    contact_data = {
        "name": "",  # Empty name should fail validation
        "email": "invalid-email",  # Invalid email format
        "subject": "Test Subject",
        "message": "Test message"
    }
    
    response = client.post("/api/v1/contact/", json=contact_data)
    
    assert response.status_code == 422  # Validation error


def test_get_contact_info(client: TestClient):
    """Test getting contact information."""
    response = client.get("/api/v1/contact/info")
    
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "phone" in data
    assert "address" in data