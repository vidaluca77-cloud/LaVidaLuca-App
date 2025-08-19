import pytest

class TestUserEndpoints:
    def test_get_current_user(self, client, auth_headers):
        """Test getting current user information."""
        response = client.get("/api/v1/users/me", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"
        assert "profile" in data

    def test_update_current_user(self, client, auth_headers):
        """Test updating current user."""
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }
        
        response = client.put("/api/v1/users/me", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"

    def test_get_current_user_profile(self, client, auth_headers):
        """Test getting current user profile."""
        response = client.get("/api/v1/users/me/profile", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "skills" in data
        assert "availability" in data
        assert "preferences" in data

    def test_update_current_user_profile(self, client, auth_headers):
        """Test updating current user profile."""
        profile_data = {
            "bio": "Updated bio",
            "skills": ["elevage", "hygiene"],
            "availability": ["weekend"],
            "preferences": ["agri", "nature"]
        }
        
        response = client.put(
            "/api/v1/users/me/profile", 
            json=profile_data, 
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["bio"] == "Updated bio"
        assert "elevage" in data["skills"]
        assert "weekend" in data["availability"]
        assert "agri" in data["preferences"]

    def test_get_user_by_id(self, client, auth_headers, test_user):
        """Test getting user by ID."""
        response = client.get(f"/api/v1/users/{test_user.id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["username"] == "testuser"

    def test_get_users_list(self, client, auth_headers):
        """Test getting list of users."""
        response = client.get("/api/v1/users/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_unauthorized_access(self, client):
        """Test that endpoints require authentication."""
        response = client.get("/api/v1/users/me")
        assert response.status_code == 401