import pytest
from fastapi.testclient import TestClient


def create_authenticated_user(client: TestClient, test_user_data):
    """Helper function to create and authenticate a user"""
    register_response = client.post("/api/auth/register", json=test_user_data)
    token = register_response.json()["token"]["access_token"]
    user_id = register_response.json()["user"]["id"]
    return token, user_id


def test_get_current_user_profile(client: TestClient, test_user_data):
    """Test getting current user profile"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["username"] == test_user_data["username"]


def test_update_current_user_profile(client: TestClient, test_user_data):
    """Test updating current user profile"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {
        "full_name": "Updated Name",
        "location": "Paris",
        "skills": ["elevage", "hygiene"],
        "availability": ["weekend"],
        "preferences": ["agri"]
    }
    
    response = client.put("/api/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["location"] == "Paris"


def test_get_user_profile_formatted(client: TestClient, test_user_data):
    """Test getting user profile in UserProfile format"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/users/me/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "skills" in data
    assert "availability" in data
    assert "location" in data
    assert "preferences" in data


def test_update_user_profile_formatted(client: TestClient, test_user_data):
    """Test updating user profile in UserProfile format"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    profile_data = {
        "skills": ["elevage", "hygiene"],
        "availability": ["weekend", "matin"],
        "location": "Lyon",
        "preferences": ["agri", "nature"]
    }
    
    response = client.put("/api/users/me/profile", json=profile_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["skills"] == profile_data["skills"]
    assert data["availability"] == profile_data["availability"]
    assert data["location"] == profile_data["location"]
    assert data["preferences"] == profile_data["preferences"]


def test_get_user_suggestions(client: TestClient, test_user_data):
    """Test getting user's activity suggestions"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/users/me/suggestions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_clear_user_suggestions(client: TestClient, test_user_data):
    """Test clearing user's activity suggestions"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/api/users/me/suggestions", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_get_user_unauthorized(client: TestClient):
    """Test getting user without authentication"""
    response = client.get("/api/users/1")
    assert response.status_code == 403


def test_get_other_user_forbidden(client: TestClient, test_user_data):
    """Test getting another user's profile (should be forbidden)"""
    token, user_id = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    # Try to access a different user (ID + 1)
    response = client.get(f"/api/users/{user_id + 1}", headers=headers)
    assert response.status_code == 403


def test_get_own_user_profile(client: TestClient, test_user_data):
    """Test getting own user profile by ID"""
    token, user_id = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id


def test_get_users_list_unauthorized(client: TestClient, test_user_data):
    """Test getting users list without admin permissions"""
    token, _ = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/api/users/", headers=headers)
    assert response.status_code == 403


def test_update_other_user_forbidden(client: TestClient, test_user_data):
    """Test updating another user's profile (should be forbidden)"""
    token, user_id = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"full_name": "Hacker Name"}
    response = client.put(f"/api/users/{user_id + 1}", json=update_data, headers=headers)
    assert response.status_code == 403


def test_delete_user_unauthorized(client: TestClient, test_user_data):
    """Test deleting user without admin permissions"""
    token, user_id = create_authenticated_user(client, test_user_data)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete(f"/api/users/{user_id}", headers=headers)
    assert response.status_code == 403