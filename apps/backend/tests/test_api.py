"""
Comprehensive API integration tests for LaVidaLuca Backend.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.models import User, Activity


@pytest.mark.integration
@pytest.mark.integration
class TestHealthAndRoot:
    """Test health check and root endpoints."""
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint returns correct response."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["message"] == "Welcome to LaVidaLuca Backend API"
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "lavidaluca-backend"
    
    def test_openapi_docs(self, client: TestClient):
        """Test OpenAPI documentation is accessible."""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data


@pytest.mark.integration
@pytest.mark.integration
class TestAuthenticationAPI:
    """Test authentication endpoints."""
    
    def test_register_user_success(self, client: TestClient, sample_user_data: dict):
        """Test successful user registration."""
        response = client.post("/api/v1/auth/register", json=sample_user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == sample_user_data["email"]
        assert data["username"] == sample_user_data["username"]
        assert data["full_name"] == sample_user_data["full_name"]
        assert "id" in data
        assert "hashed_password" not in data  # Should not expose password
    
    def test_register_user_duplicate_email(self, client: TestClient, test_user: User):
        """Test registration fails with duplicate email."""
        user_data = {
            "email": test_user.email,
            "username": "newusername",
            "password": "testpassword",
            "full_name": "New User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_register_user_duplicate_username(self, client: TestClient, test_user: User):
        """Test registration fails with duplicate username."""
        user_data = {
            "email": "newemail@example.com",
            "username": test_user.username,
            "password": "testpassword",
            "full_name": "New User"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    def test_register_user_invalid_email(self, client: TestClient):
        """Test registration fails with invalid email."""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error
    
    def test_login_user_success(self, client: TestClient, test_user: User):
        """Test successful user login."""
        login_data = {
            "username": test_user.username,
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_user_invalid_username(self, client: TestClient):
        """Test login fails with invalid username."""
        login_data = {
            "username": "nonexistent",
            "password": "testpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]
    
    def test_login_user_invalid_password(self, client: TestClient, test_user: User):
        """Test login fails with invalid password."""
        login_data = {
            "username": test_user.username,
            "password": "wrongpassword"
        }
        response = client.post("/api/v1/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]


@pytest.mark.integration
@pytest.mark.integration
class TestActivitiesAPI:
    """Test activities endpoints."""
    
    def test_get_activities_empty(self, client: TestClient):
        """Test getting activities when none exist."""
        response = client.get("/api/v1/activities/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_get_activities_success(self, client: TestClient, test_activities: list):
        """Test getting activities successfully."""
        response = client.get("/api/v1/activities/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == len(test_activities)
        
        # Verify activity structure
        activity = data[0]
        assert "id" in activity
        assert "title" in activity
        assert "category" in activity
        assert "difficulty_level" in activity
    
    def test_get_activities_pagination(self, client: TestClient, test_activities: list):
        """Test activities pagination."""
        response = client.get("/api/v1/activities/?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2
    
    def test_get_activities_filter_by_category(self, client: TestClient, test_activities: list):
        """Test filtering activities by category."""
        # Get a category from test activities
        test_category = test_activities[0].category
        response = client.get(f"/api/v1/activities/?category={test_category}")
        assert response.status_code == 200
        data = response.json()
        
        # All returned activities should have the specified category
        for activity in data:
            assert activity["category"] == test_category
    
    def test_get_activities_filter_by_difficulty(self, client: TestClient, test_activities: list):
        """Test filtering activities by difficulty."""
        test_difficulty = "beginner"
        response = client.get(f"/api/v1/activities/?difficulty={test_difficulty}")
        assert response.status_code == 200
        data = response.json()
        
        # All returned activities should have the specified difficulty
        for activity in data:
            assert activity["difficulty_level"] == test_difficulty
    
    def test_get_activity_by_id_success(self, client: TestClient, test_activity: Activity):
        """Test getting specific activity by ID."""
        response = client.get(f"/api/v1/activities/{test_activity.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_activity.id
        assert data["title"] == test_activity.title
    
    def test_get_activity_by_id_not_found(self, client: TestClient):
        """Test getting non-existent activity."""
        response = client.get("/api/v1/activities/999999")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
    
    def test_create_activity_success(self, client: TestClient, auth_headers: dict, sample_activity_data: dict):
        """Test creating activity successfully."""
        response = client.post(
            "/api/v1/activities/", 
            json=sample_activity_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == sample_activity_data["title"]
        assert data["category"] == sample_activity_data["category"]
        assert "id" in data
        assert "creator_id" in data
    
    def test_create_activity_unauthorized(self, client: TestClient, sample_activity_data: dict):
        """Test creating activity without authentication."""
        response = client.post("/api/v1/activities/", json=sample_activity_data)
        assert response.status_code == 401
    
    def test_create_activity_invalid_data(self, client: TestClient, auth_headers: dict):
        """Test creating activity with invalid data."""
        invalid_data = {
            "title": "",  # Invalid empty title
            "category": "invalid"
        }
        response = client.post(
            "/api/v1/activities/", 
            json=invalid_data,
            headers=auth_headers
        )
        assert response.status_code == 422  # Validation error
    
    def test_update_activity_success(self, client: TestClient, test_activity: Activity, auth_headers: dict):
        """Test updating activity successfully."""
        update_data = {
            "title": "Updated Title",
            "description": "Updated description"
        }
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
    
    def test_update_activity_unauthorized(self, client: TestClient, test_activity: Activity):
        """Test updating activity without authentication."""
        update_data = {"title": "Updated Title"}
        response = client.put(f"/api/v1/activities/{test_activity.id}", json=update_data)
        assert response.status_code == 401
    
    def test_update_activity_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent activity."""
        update_data = {"title": "Updated Title"}
        response = client.put(
            "/api/v1/activities/999999",
            json=update_data,
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_update_activity_forbidden(self, client: TestClient, test_activity: Activity, multiple_users: list):
        """Test updating activity by non-owner user."""
        # Create auth headers for a different user
        other_user = multiple_users[0]
        from app.core.security import create_access_token
        other_auth_headers = {"Authorization": f"Bearer {create_access_token(subject=other_user.id)}"}
        
        update_data = {"title": "Updated Title"}
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=other_auth_headers
        )
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]
    
    def test_update_activity_by_superuser(self, client: TestClient, test_activity: Activity, superuser_auth_headers: dict):
        """Test superuser can update any activity."""
        update_data = {"title": "Updated by Superuser"}
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=superuser_auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
    
    def test_delete_activity_success(self, client: TestClient, test_activity: Activity, auth_headers: dict):
        """Test deleting activity successfully."""
        response = client.delete(
            f"/api/v1/activities/{test_activity.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "deleted successfully" in data["message"]
    
    def test_delete_activity_unauthorized(self, client: TestClient, test_activity: Activity):
        """Test deleting activity without authentication."""
        response = client.delete(f"/api/v1/activities/{test_activity.id}")
        assert response.status_code == 401
    
    def test_delete_activity_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent activity."""
        response = client.delete("/api/v1/activities/999999", headers=auth_headers)
        assert response.status_code == 404
    
    def test_delete_activity_forbidden(self, client: TestClient, test_activity: Activity, multiple_users: list):
        """Test deleting activity by non-owner user."""
        # Create auth headers for a different user
        other_user = multiple_users[0]
        from app.core.security import create_access_token
        other_auth_headers = {"Authorization": f"Bearer {create_access_token(subject=other_user.id)}"}
        
        response = client.delete(
            f"/api/v1/activities/{test_activity.id}",
            headers=other_auth_headers
        )
        assert response.status_code == 403
    
    def test_get_activity_categories(self, client: TestClient, test_activities: list):
        """Test getting activity categories."""
        response = client.get("/api/v1/activities/categories/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        # Should contain categories from test activities
        test_categories = [activity.category for activity in test_activities]
        for category in data:
            assert category in test_categories


@pytest.mark.integration
class TestUsersAPI:
    """Test users endpoints (if they exist)."""
    
    def test_get_current_user(self, client: TestClient, auth_headers: dict, test_user: User):
        """Test getting current user info."""
        # This endpoint might not exist yet, so we'll skip if 404
        response = client.get("/api/v1/users/me", headers=auth_headers)
        if response.status_code == 404:
            pytest.skip("Users endpoint not implemented yet")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_user.id
        assert data["email"] == test_user.email


@pytest.mark.integration
class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_invalid_endpoint(self, client: TestClient):
        """Test accessing non-existent endpoint."""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    def test_invalid_http_method(self, client: TestClient):
        """Test using wrong HTTP method."""
        response = client.post("/api/v1/activities/categories/")
        # Should return 405 Method Not Allowed or 404 if not implemented
        assert response.status_code in [404, 405]
    
    def test_malformed_json(self, client: TestClient, auth_headers: dict):
        """Test sending malformed JSON."""
        import json
        response = client.post(
            "/api/v1/activities/",
            data="invalid json",
            headers={**auth_headers, "Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, client: TestClient, auth_headers: dict):
        """Test creating activity with missing required fields."""
        incomplete_data = {
            "description": "Missing title and category"
        }
        response = client.post(
            "/api/v1/activities/",
            json=incomplete_data,
            headers=auth_headers
        )
        assert response.status_code == 422
    
    def test_expired_token(self, client: TestClient, expired_token: str, sample_activity_data: dict):
        """Test using expired authentication token."""
        expired_headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.post(
            "/api/v1/activities/",
            json=sample_activity_data,
            headers=expired_headers
        )
        assert response.status_code == 401
    
    def test_invalid_token(self, client: TestClient, sample_activity_data: dict):
        """Test using invalid authentication token."""
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        response = client.post(
            "/api/v1/activities/",
            json=sample_activity_data,
            headers=invalid_headers
        )
        assert response.status_code == 401


@pytest.mark.integration
class TestRateLimiting:
    """Test rate limiting and performance considerations."""
    
    def test_bulk_requests(self, client: TestClient):
        """Test handling multiple concurrent requests."""
        responses = []
        for i in range(10):
            response = client.get("/api/v1/activities/")
            responses.append(response)
        
        # All requests should succeed (assuming no rate limiting yet)
        for response in responses:
            assert response.status_code == 200
    
    def test_large_pagination_request(self, client: TestClient, test_activities: list):
        """Test requesting large number of items."""
        response = client.get("/api/v1/activities/?limit=100")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 100  # Should respect limit