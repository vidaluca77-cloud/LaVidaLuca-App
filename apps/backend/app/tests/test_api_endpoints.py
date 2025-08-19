"""
Comprehensive API endpoint tests for LaVidaLuca backend.

Tests all API endpoints including users, activities, suggestions, and error handling.
"""

import pytest
import json
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock

from app.models.user import User
from app.models.activity import Activity


class TestAPIAuthentication:
    """Test API authentication requirements."""

    def test_protected_endpoints_require_auth(self, client: TestClient):
        """Test that protected endpoints require authentication."""
        protected_endpoints = [
            ("GET", "/api/v1/users/me"),
            ("PUT", "/api/v1/users/me"),
            ("GET", "/api/v1/users/"),
            ("POST", "/api/v1/activities/"),
            ("GET", "/api/v1/activities/my"),
            ("PUT", "/api/v1/activities/123"),
            ("DELETE", "/api/v1/activities/123"),
            ("POST", "/api/v1/suggestions/generate"),
        ]
        
        for method, endpoint in protected_endpoints:
            response = getattr(client, method.lower())(endpoint)
            assert response.status_code == 401, f"{method} {endpoint} should require auth"

    def test_public_endpoints_no_auth_required(self, client: TestClient):
        """Test that public endpoints don't require authentication."""
        public_endpoints = [
            ("GET", "/"),
            ("GET", "/health"),
            ("POST", "/api/v1/auth/register"),
            ("POST", "/api/v1/auth/login"),
            ("GET", "/api/v1/activities/"),  # Public activity list
            ("GET", "/api/v1/activities/123"),  # Public activity details
        ]
        
        for method, endpoint in public_endpoints:
            response = getattr(client, method.lower())(endpoint)
            # Should not return 401 (may return 404 or other status)
            assert response.status_code != 401, f"{method} {endpoint} should not require auth"


class TestUserEndpoints:
    """Test user-related API endpoints."""

    def setup_method(self):
        """Set up test data."""
        self.user_data = {
            "email": "apitest@example.com",
            "password": "TestPassword123!",
            "first_name": "API",
            "last_name": "Test"
        }

    def get_auth_headers(self, client: TestClient) -> dict:
        """Get authentication headers for test user."""
        # Register and login user
        client.post("/api/v1/auth/register", json=self.user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        token = login_response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_get_current_user(self, client: TestClient):
        """Test getting current user information."""
        headers = self.get_auth_headers(client)
        
        response = client.get("/api/v1/users/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["email"] == self.user_data["email"]
        assert data["data"]["first_name"] == self.user_data["first_name"]
        assert "id" in data["data"]

    def test_update_current_user(self, client: TestClient):
        """Test updating current user information."""
        headers = self.get_auth_headers(client)
        
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "profile": {
                "bio": "Updated bio",
                "location": "New Location"
            }
        }
        
        response = client.put("/api/v1/users/me", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["first_name"] == "Updated"
        assert data["data"]["last_name"] == "Name"
        assert data["data"]["profile"]["bio"] == "Updated bio"

    def test_update_user_invalid_data(self, client: TestClient):
        """Test updating user with invalid data."""
        headers = self.get_auth_headers(client)
        
        invalid_updates = [
            {"email": "invalid-email"},  # Invalid email format
            {"first_name": ""},  # Empty name
            {"profile": "not-a-dict"},  # Invalid profile type
        ]
        
        for update_data in invalid_updates:
            response = client.put("/api/v1/users/me", json=update_data, headers=headers)
            assert response.status_code == 422

    def test_get_user_list_admin_only(self, client: TestClient):
        """Test that user list is admin-only."""
        headers = self.get_auth_headers(client)
        
        response = client.get("/api/v1/users/", headers=headers)
        
        # Should return 403 for non-admin users
        assert response.status_code == 403

    def test_change_password(self, client: TestClient):
        """Test password change functionality."""
        headers = self.get_auth_headers(client)
        
        password_data = {
            "current_password": self.user_data["password"],
            "new_password": "NewPassword123!"
        }
        
        response = client.post("/api/v1/users/change-password", 
                             json=password_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Test login with new password
        login_response = client.post("/api/v1/auth/login", json={
            "email": self.user_data["email"],
            "password": "NewPassword123!"
        })
        assert login_response.status_code == 200

    def test_change_password_wrong_current(self, client: TestClient):
        """Test password change with wrong current password."""
        headers = self.get_auth_headers(client)
        
        password_data = {
            "current_password": "WrongPassword",
            "new_password": "NewPassword123!"
        }
        
        response = client.post("/api/v1/users/change-password", 
                             json=password_data, headers=headers)
        
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False


class TestActivityEndpoints:
    """Test activity-related API endpoints."""

    def setup_method(self):
        """Set up test data."""
        self.user_data = {
            "email": "activitytest@example.com",
            "password": "TestPassword123!",
            "first_name": "Activity",
            "last_name": "Test"
        }
        self.activity_data = {
            "title": "Test Activity",
            "description": "A comprehensive test activity",
            "category": "test",
            "difficulty_level": "intermediate",
            "estimated_duration": 60,
            "materials": ["Test material 1", "Test material 2"],
            "instructions": [
                "Step 1: Do something",
                "Step 2: Do something else"
            ],
            "tags": ["test", "api", "activity"]
        }

    def get_auth_headers(self, client: TestClient) -> dict:
        """Get authentication headers for test user."""
        client.post("/api/v1/auth/register", json=self.user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        token = login_response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_create_activity(self, client: TestClient):
        """Test creating a new activity."""
        headers = self.get_auth_headers(client)
        
        response = client.post("/api/v1/activities/", 
                             json=self.activity_data, headers=headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == self.activity_data["title"]
        assert data["data"]["description"] == self.activity_data["description"]
        assert data["data"]["category"] == self.activity_data["category"]
        assert "id" in data["data"]
        assert "created_at" in data["data"]

    def test_create_activity_invalid_data(self, client: TestClient):
        """Test creating activity with invalid data."""
        headers = self.get_auth_headers(client)
        
        invalid_activities = [
            {},  # Empty data
            {"title": ""},  # Empty title
            {"title": "Test", "difficulty_level": "invalid"},  # Invalid difficulty
            {"title": "Test", "estimated_duration": -1},  # Negative duration
            {"title": "Test", "category": ""},  # Empty category
        ]
        
        for activity_data in invalid_activities:
            response = client.post("/api/v1/activities/", 
                                 json=activity_data, headers=headers)
            assert response.status_code == 422

    def test_get_activity_list(self, client: TestClient):
        """Test getting list of activities."""
        headers = self.get_auth_headers(client)
        
        # Create a few test activities
        for i in range(3):
            activity_data = self.activity_data.copy()
            activity_data["title"] = f"Test Activity {i}"
            client.post("/api/v1/activities/", json=activity_data, headers=headers)
        
        # Get activity list
        response = client.get("/api/v1/activities/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) >= 3
        assert all("title" in activity for activity in data["data"])

    def test_get_activity_list_with_filters(self, client: TestClient):
        """Test getting activities with filters."""
        headers = self.get_auth_headers(client)
        
        # Create activities with different categories
        categories = ["sports", "art", "cooking"]
        for category in categories:
            activity_data = self.activity_data.copy()
            activity_data["category"] = category
            activity_data["title"] = f"{category.title()} Activity"
            client.post("/api/v1/activities/", json=activity_data, headers=headers)
        
        # Test category filter
        response = client.get("/api/v1/activities/?category=sports")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert all(activity["category"] == "sports" for activity in data["data"])

    def test_get_activity_list_pagination(self, client: TestClient):
        """Test activity list pagination."""
        headers = self.get_auth_headers(client)
        
        # Create many activities
        for i in range(15):
            activity_data = self.activity_data.copy()
            activity_data["title"] = f"Pagination Test Activity {i}"
            client.post("/api/v1/activities/", json=activity_data, headers=headers)
        
        # Test pagination
        response = client.get("/api/v1/activities/?page=1&size=10")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) <= 10
        assert "pagination" in data

    def test_get_activity_by_id(self, client: TestClient):
        """Test getting specific activity by ID."""
        headers = self.get_auth_headers(client)
        
        # Create activity
        create_response = client.post("/api/v1/activities/", 
                                    json=self.activity_data, headers=headers)
        activity_id = create_response.json()["data"]["id"]
        
        # Get activity by ID
        response = client.get(f"/api/v1/activities/{activity_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["id"] == activity_id
        assert data["data"]["title"] == self.activity_data["title"]

    def test_get_nonexistent_activity(self, client: TestClient):
        """Test getting non-existent activity."""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/api/v1/activities/{fake_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["success"] is False

    def test_update_activity(self, client: TestClient):
        """Test updating an activity."""
        headers = self.get_auth_headers(client)
        
        # Create activity
        create_response = client.post("/api/v1/activities/", 
                                    json=self.activity_data, headers=headers)
        activity_id = create_response.json()["data"]["id"]
        
        # Update activity
        update_data = {
            "title": "Updated Activity Title",
            "description": "Updated description",
            "difficulty_level": "advanced"
        }
        
        response = client.put(f"/api/v1/activities/{activity_id}", 
                            json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["title"] == "Updated Activity Title"
        assert data["data"]["description"] == "Updated description"
        assert data["data"]["difficulty_level"] == "advanced"

    def test_update_activity_unauthorized(self, client: TestClient):
        """Test updating activity by different user."""
        # Create activity with first user
        headers1 = self.get_auth_headers(client)
        create_response = client.post("/api/v1/activities/", 
                                    json=self.activity_data, headers=headers1)
        activity_id = create_response.json()["data"]["id"]
        
        # Try to update with different user
        user2_data = {
            "email": "user2@example.com",
            "password": "TestPassword123!",
            "first_name": "User",
            "last_name": "Two"
        }
        client.post("/api/v1/auth/register", json=user2_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": user2_data["email"],
            "password": user2_data["password"]
        })
        token2 = login_response.json()["data"]["access_token"]
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        update_data = {"title": "Unauthorized Update"}
        response = client.put(f"/api/v1/activities/{activity_id}", 
                            json=update_data, headers=headers2)
        
        assert response.status_code == 403

    def test_delete_activity(self, client: TestClient):
        """Test deleting an activity."""
        headers = self.get_auth_headers(client)
        
        # Create activity
        create_response = client.post("/api/v1/activities/", 
                                    json=self.activity_data, headers=headers)
        activity_id = create_response.json()["data"]["id"]
        
        # Delete activity
        response = client.delete(f"/api/v1/activities/{activity_id}", 
                               headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify activity is deleted
        get_response = client.get(f"/api/v1/activities/{activity_id}")
        assert get_response.status_code == 404

    def test_get_my_activities(self, client: TestClient):
        """Test getting current user's activities."""
        headers = self.get_auth_headers(client)
        
        # Create activities for current user
        activity_ids = []
        for i in range(3):
            activity_data = self.activity_data.copy()
            activity_data["title"] = f"My Activity {i}"
            response = client.post("/api/v1/activities/", 
                                 json=activity_data, headers=headers)
            activity_ids.append(response.json()["data"]["id"])
        
        # Get my activities
        response = client.get("/api/v1/activities/my", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 3
        
        returned_ids = [activity["id"] for activity in data["data"]]
        assert all(aid in returned_ids for aid in activity_ids)


class TestSuggestionEndpoints:
    """Test suggestion-related API endpoints."""

    def setup_method(self):
        """Set up test data."""
        self.user_data = {
            "email": "suggestiontest@example.com",
            "password": "TestPassword123!",
            "first_name": "Suggestion",
            "last_name": "Test"
        }

    def get_auth_headers(self, client: TestClient) -> dict:
        """Get authentication headers for test user."""
        client.post("/api/v1/auth/register", json=self.user_data)
        login_response = client.post("/api/v1/auth/login", json={
            "email": self.user_data["email"],
            "password": self.user_data["password"]
        })
        token = login_response.json()["data"]["access_token"]
        return {"Authorization": f"Bearer {token}"}

    @patch('app.services.openai_service.OpenAIService.generate_suggestions')
    def test_generate_suggestions(self, mock_openai, client: TestClient):
        """Test generating activity suggestions."""
        headers = self.get_auth_headers(client)
        
        # Mock OpenAI response
        mock_openai.return_value = [
            {
                "title": "Mock Activity 1",
                "description": "Mock description 1",
                "category": "test",
                "difficulty_level": "beginner",
                "estimated_duration": 30
            },
            {
                "title": "Mock Activity 2",
                "description": "Mock description 2",
                "category": "test",
                "difficulty_level": "intermediate",
                "estimated_duration": 45
            }
        ]
        
        suggestion_data = {
            "preferences": {
                "categories": ["sports", "art"],
                "difficulty_level": "beginner",
                "max_duration": 60
            },
            "context": "Looking for indoor activities for rainy day"
        }
        
        response = client.post("/api/v1/suggestions/generate", 
                             json=suggestion_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]) == 2
        assert data["data"][0]["title"] == "Mock Activity 1"

    def test_generate_suggestions_invalid_data(self, client: TestClient):
        """Test generating suggestions with invalid data."""
        headers = self.get_auth_headers(client)
        
        invalid_requests = [
            {},  # Empty data
            {"preferences": {}},  # Empty preferences
            {"preferences": {"difficulty_level": "invalid"}},  # Invalid difficulty
            {"preferences": {"max_duration": -1}},  # Invalid duration
        ]
        
        for suggestion_data in invalid_requests:
            response = client.post("/api/v1/suggestions/generate", 
                                 json=suggestion_data, headers=headers)
            assert response.status_code == 422

    @patch('app.services.openai_service.OpenAIService.generate_suggestions')
    def test_generate_suggestions_openai_error(self, mock_openai, client: TestClient):
        """Test handling OpenAI service errors."""
        headers = self.get_auth_headers(client)
        
        # Mock OpenAI error
        mock_openai.side_effect = Exception("OpenAI API error")
        
        suggestion_data = {
            "preferences": {
                "categories": ["sports"],
                "difficulty_level": "beginner"
            }
        }
        
        response = client.post("/api/v1/suggestions/generate", 
                             json=suggestion_data, headers=headers)
        
        assert response.status_code == 500
        data = response.json()
        assert data["success"] is False


class TestErrorHandling:
    """Test API error handling and edge cases."""

    def test_404_not_found(self, client: TestClient):
        """Test 404 handling for non-existent endpoints."""
        response = client.get("/api/v1/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_405_method_not_allowed(self, client: TestClient):
        """Test 405 handling for unsupported methods."""
        response = client.patch("/api/v1/auth/login")  # PATCH not supported
        
        assert response.status_code == 405

    def test_422_validation_error(self, client: TestClient):
        """Test 422 handling for validation errors."""
        invalid_data = {
            "email": "not-an-email",
            "password": "short"
        }
        
        response = client.post("/api/v1/auth/register", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)

    def test_500_internal_server_error(self, client: TestClient):
        """Test 500 handling for internal errors."""
        # This would be triggered by actual server errors
        # For now, we just ensure the error handling structure is in place
        pass

    def test_invalid_json_request(self, client: TestClient):
        """Test handling of invalid JSON in request body."""
        response = client.post(
            "/api/v1/auth/login",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422

    def test_missing_content_type(self, client: TestClient):
        """Test handling of missing content type for JSON endpoints."""
        response = client.post(
            "/api/v1/auth/login",
            data='{"email": "test@example.com", "password": "password"}'
        )
        
        # Should either work or return appropriate error
        assert response.status_code in [200, 400, 422]

    def test_large_request_body(self, client: TestClient):
        """Test handling of overly large request bodies."""
        large_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "A" * 10000,  # Very long name
            "last_name": "Test"
        }
        
        response = client.post("/api/v1/auth/register", json=large_data)
        
        # Should return validation error for field length
        assert response.status_code == 422


class TestAPIPerformance:
    """Test API performance and response times."""

    def test_response_time_health_check(self, client: TestClient):
        """Test health check response time."""
        import time
        
        start_time = time.time()
        response = client.get("/health")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second

    def test_response_time_activity_list(self, client: TestClient):
        """Test activity list response time."""
        import time
        
        start_time = time.time()
        response = client.get("/api/v1/activities/")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should respond within 2 seconds

    def test_concurrent_requests(self, client: TestClient):
        """Test handling of concurrent requests."""
        import concurrent.futures
        import threading
        
        def make_request():
            return client.get("/health")
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(response.status_code == 200 for response in results)