import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_get_activities(client: TestClient):
    """Test getting all activities."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase:
        mock_activities = [
            {
                "id": "activity-1",
                "title": "Test Activity 1",
                "slug": "test-activity-1",
                "category": "agri",
                "summary": "Test summary 1",
                "duration_min": 60,
                "skill_tags": ["test"],
                "seasonality": ["printemps"],
                "safety_level": 1,
                "materials": ["gants"],
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        ]
        mock_supabase.return_value.table.return_value.select.return_value.range.return_value.execute.return_value.data = mock_activities
        
        response = client.get("/api/v1/activities/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Activity 1"

def test_get_activities_with_filters(client: TestClient):
    """Test getting activities with filters."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase:
        mock_activities = []
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.range.return_value.execute.return_value.data = mock_activities
        
        response = client.get("/api/v1/activities/?category=agri&limit=10&offset=0")
        assert response.status_code == 200

def test_get_activity_by_id(client: TestClient):
    """Test getting a specific activity."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase:
        mock_activity = {
            "id": "activity-1",
            "title": "Test Activity",
            "slug": "test-activity",
            "category": "agri",
            "summary": "Test summary",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["printemps"],
            "safety_level": 1,
            "materials": ["gants"],
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00"
        }
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [mock_activity]
        
        response = client.get("/api/v1/activities/activity-1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "activity-1"
        assert data["title"] == "Test Activity"

def test_get_activity_not_found(client: TestClient):
    """Test getting a non-existent activity."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase:
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        response = client.get("/api/v1/activities/non-existent")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

def test_create_activity(client: TestClient, test_activity_data):
    """Test creating a new activity."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase, \
         patch('app.routers.activities.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        
        # Mock no existing activity with same slug
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        # Mock successful insert
        mock_activity_response = {**test_activity_data, "id": "new-activity-id", "created_at": "2024-01-01T00:00:00", "updated_at": "2024-01-01T00:00:00"}
        mock_supabase.return_value.table.return_value.insert.return_value.execute.return_value.data = [mock_activity_response]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post("/api/v1/activities/", json=test_activity_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == test_activity_data["title"]
        assert data["slug"] == test_activity_data["slug"]

def test_create_activity_duplicate_slug(client: TestClient, test_activity_data):
    """Test creating activity with duplicate slug."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase, \
         patch('app.routers.activities.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        
        # Mock existing activity with same slug
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": "existing-id"}]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post("/api/v1/activities/", json=test_activity_data, headers=headers)
        assert response.status_code == 400
        assert "Activity with this slug already exists" in response.json()["detail"]

def test_update_activity(client: TestClient):
    """Test updating an activity."""
    update_data = {"title": "Updated Activity Title"}
    
    with patch('app.routers.activities.get_supabase_client') as mock_supabase, \
         patch('app.routers.activities.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        
        # Mock existing activity
        mock_existing = {"id": "activity-1", "title": "Old Title"}
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [mock_existing]
        
        # Mock successful update
        mock_updated = {**mock_existing, **update_data, "updated_at": "2024-01-01T00:00:00"}
        mock_supabase.return_value.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [mock_updated]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.put("/api/v1/activities/activity-1", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Activity Title"

def test_delete_activity(client: TestClient):
    """Test deleting an activity."""
    with patch('app.routers.activities.get_supabase_client') as mock_supabase, \
         patch('app.routers.activities.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        
        # Mock existing activity
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{"id": "activity-1"}]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.delete("/api/v1/activities/activity-1", headers=headers)
        assert response.status_code == 204