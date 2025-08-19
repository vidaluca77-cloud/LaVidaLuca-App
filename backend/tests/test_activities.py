"""
Tests for activities endpoints.
"""

import pytest
from httpx import AsyncClient


class TestActivities:
    """Test activities endpoints."""
    
    async def test_get_activities_list(self, client: AsyncClient, test_activity):
        """Test getting list of activities."""
        response = await client.get("/api/activities/")
        
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data
        assert data["total"] >= 1
        assert len(data["items"]) >= 1
        
        activity = data["items"][0]
        assert activity["id"] == test_activity.id
        assert activity["title"] == test_activity.title
    
    async def test_get_activities_with_filters(self, client: AsyncClient, test_activity):
        """Test getting activities with filters."""
        response = await client.get("/api/activities/", params={
            "category": "agri",
            "duration_min_max": 120,
            "safety_level_max": 3
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
    
    async def test_get_activities_with_search(self, client: AsyncClient, test_activity):
        """Test getting activities with search."""
        response = await client.get("/api/activities/", params={
            "search": "Test"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert "Test" in data["items"][0]["title"]
    
    async def test_get_activities_pagination(self, client: AsyncClient, test_activity):
        """Test activities pagination."""
        response = await client.get("/api/activities/", params={
            "page": 1,
            "size": 10
        })
        
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 10
        assert data["pages"] >= 1
    
    async def test_get_activity_by_id(self, client: AsyncClient, test_activity):
        """Test getting specific activity by ID."""
        response = await client.get(f"/api/activities/{test_activity.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_activity.id
        assert data["title"] == test_activity.title
        assert data["category"] == test_activity.category
    
    async def test_get_nonexistent_activity(self, client: AsyncClient):
        """Test getting nonexistent activity."""
        response = await client.get("/api/activities/nonexistent-id")
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]
    
    async def test_create_activity(self, client: AsyncClient, auth_headers, sample_activity_data):
        """Test creating new activity."""
        response = await client.post(
            "/api/activities/",
            json=sample_activity_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "activity_id" in data["data"]
        assert data["message"] == "Activity created successfully"
    
    async def test_create_activity_unauthorized(self, client: AsyncClient, sample_activity_data):
        """Test creating activity without authentication."""
        response = await client.post("/api/activities/", json=sample_activity_data)
        
        assert response.status_code == 403
    
    async def test_create_activity_invalid_data(self, client: AsyncClient, auth_headers):
        """Test creating activity with invalid data."""
        invalid_data = {
            "title": "",  # Empty title
            "category": "invalid_category",
            "summary": "Test summary"
            # Missing required fields
        }
        
        response = await client.post(
            "/api/activities/",
            json=invalid_data,
            headers=auth_headers
        )
        
        assert response.status_code == 422  # Validation error
    
    async def test_update_activity(self, client: AsyncClient, test_activity, auth_headers):
        """Test updating an activity."""
        update_data = {
            "title": "Updated Test Activity",
            "summary": "Updated summary",
            "duration_min": 90
        }
        
        response = await client.put(
            f"/api/activities/{test_activity.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Activity updated successfully"
    
    async def test_update_nonexistent_activity(self, client: AsyncClient, auth_headers):
        """Test updating nonexistent activity."""
        update_data = {"title": "Updated Title"}
        
        response = await client.put(
            "/api/activities/nonexistent-id",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_update_activity_unauthorized(self, client: AsyncClient, test_activity):
        """Test updating activity without authentication."""
        update_data = {"title": "Updated Title"}
        
        response = await client.put(
            f"/api/activities/{test_activity.id}",
            json=update_data
        )
        
        assert response.status_code == 403
    
    async def test_delete_activity(self, client: AsyncClient, test_activity, auth_headers):
        """Test deleting an activity."""
        response = await client.delete(
            f"/api/activities/{test_activity.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Activity deleted successfully"
        
        # Verify activity is deleted
        get_response = await client.get(f"/api/activities/{test_activity.id}")
        assert get_response.status_code == 404
    
    async def test_delete_nonexistent_activity(self, client: AsyncClient, auth_headers):
        """Test deleting nonexistent activity."""
        response = await client.delete(
            "/api/activities/nonexistent-id",
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    async def test_delete_activity_unauthorized(self, client: AsyncClient, test_activity):
        """Test deleting activity without authentication."""
        response = await client.delete(f"/api/activities/{test_activity.id}")
        
        assert response.status_code == 403
    
    async def test_get_activity_categories(self, client: AsyncClient):
        """Test getting available activity categories."""
        response = await client.get("/api/activities/categories/list")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "agri" in data
        assert "transfo" in data
        assert "artisanat" in data
        assert "nature" in data
        assert "social" in data