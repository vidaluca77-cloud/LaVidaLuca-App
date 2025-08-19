import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

def test_get_user_registrations(client: TestClient):
    """Test getting current user's registrations."""
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock registrations with activities
        mock_registrations = [
            {
                "id": "reg-1",
                "user_id": "user-1",
                "activity_id": "activity-1",
                "status": "pending",
                "notes": "Test notes",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
                "activities": {
                    "id": "activity-1",
                    "title": "Test Activity",
                    "category": "agri",
                    "summary": "Test summary",
                    "duration_min": 60
                }
            }
        ]
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.range.return_value.execute.return_value.data = mock_registrations
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.get("/api/v1/registrations/", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "reg-1"

def test_get_registration_by_id(client: TestClient):
    """Test getting a specific registration."""
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock registration
        mock_registration = {
            "id": "reg-1",
            "user_id": "user-1",
            "activity_id": "activity-1",
            "status": "pending",
            "notes": "Test notes",
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
            "activities": {
                "id": "activity-1",
                "title": "Test Activity",
                "category": "agri"
            }
        }
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [mock_registration]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.get("/api/v1/registrations/reg-1", headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "reg-1"

def test_create_registration(client: TestClient):
    """Test creating a new registration."""
    registration_data = {
        "activity_id": "activity-1",
        "notes": "I'm interested in this activity"
    }
    
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock activity exists
        mock_activity = {"id": "activity-1", "title": "Test Activity"}
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[mock_activity]),  # Activity check
            MagicMock(data=[]),  # No existing registration
            MagicMock(data=[{  # Insert response
                "id": "reg-1",
                "user_id": "user-1",
                "activity_id": "activity-1",
                "status": "pending",
                "notes": "I'm interested in this activity",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }]),
            MagicMock(data=[{  # Full response with activity
                "id": "reg-1",
                "user_id": "user-1",
                "activity_id": "activity-1",
                "status": "pending",
                "notes": "I'm interested in this activity",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00",
                "activities": mock_activity
            }])
        ]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post("/api/v1/registrations/", json=registration_data, headers=headers)
        assert response.status_code == 201
        data = response.json()
        assert data["activity_id"] == "activity-1"
        assert data["notes"] == "I'm interested in this activity"

def test_create_registration_activity_not_found(client: TestClient):
    """Test creating registration for non-existent activity."""
    registration_data = {"activity_id": "non-existent", "notes": "Test"}
    
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock activity doesn't exist
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post("/api/v1/registrations/", json=registration_data, headers=headers)
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

def test_create_registration_already_exists(client: TestClient):
    """Test creating registration when already registered."""
    registration_data = {"activity_id": "activity-1", "notes": "Test"}
    
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock activity exists and existing registration
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[{"id": "activity-1"}]),  # Activity exists
            MagicMock(data=[{"id": "existing-reg"}])  # Existing registration
        ]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.post("/api/v1/registrations/", json=registration_data, headers=headers)
        assert response.status_code == 400
        assert "Already registered" in response.json()["detail"]

def test_update_registration(client: TestClient):
    """Test updating a registration."""
    update_data = {"status": "confirmed", "notes": "Updated notes"}
    
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock existing registration and update
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.side_effect = [
            MagicMock(data=[{"id": "reg-1", "user_id": "user-1"}]),  # Existing registration
            MagicMock(data=[{  # Updated registration with activity
                "id": "reg-1",
                "user_id": "user-1",
                "activity_id": "activity-1",
                "status": "confirmed",
                "notes": "Updated notes",
                "activities": {"id": "activity-1", "title": "Test Activity"}
            }])
        ]
        mock_supabase.return_value.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [{"id": "reg-1"}]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.put("/api/v1/registrations/reg-1", json=update_data, headers=headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "confirmed"

def test_delete_registration(client: TestClient):
    """Test deleting a registration."""
    with patch('app.routers.registrations.get_supabase_client') as mock_supabase, \
         patch('app.routers.registrations.get_current_active_user') as mock_get_user:
        
        # Mock user authentication
        mock_user = MagicMock()
        mock_user.id = "user-1"
        mock_get_user.return_value = mock_user
        
        # Mock existing registration
        mock_supabase.return_value.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value.data = [{"id": "reg-1"}]
        
        headers = {"Authorization": "Bearer test-token"}
        response = client.delete("/api/v1/registrations/reg-1", headers=headers)
        assert response.status_code == 204