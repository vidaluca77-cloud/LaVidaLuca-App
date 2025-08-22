import pytest

class TestActivityEndpoints:
    def test_get_activities(self, client):
        """Test getting list of activities (public endpoint)."""
        response = client.get("/api/v1/activities/")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_activities_with_filters(self, client, test_activity):
        """Test getting activities with filters."""
        # Filter by category
        response = client.get("/api/v1/activities/?category=agri")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "agri"

    def test_get_activity_by_id(self, client, test_activity):
        """Test getting activity by ID."""
        response = client.get(f"/api/v1/activities/{test_activity.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_activity.id
        assert data["title"] == "Test Activity"
        assert "sessions" in data

    def test_get_activity_by_slug(self, client, test_activity):
        """Test getting activity by slug."""
        response = client.get(f"/api/v1/activities/slug/{test_activity.slug}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == test_activity.slug
        assert data["title"] == "Test Activity"

    def test_get_recommendations(self, client, auth_headers, test_activity):
        """Test getting activity recommendations."""
        response = client.get("/api/v1/activities/recommendations", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_activity(self, client, auth_headers):
        """Test creating new activity."""
        activity_data = {
            "slug": "new-test-activity",
            "title": "New Test Activity",
            "category": "transfo",
            "summary": "A new test activity",
            "duration_min": 120,
            "safety_level": 2,
            "skill_tags": ["precision"],
            "seasonality": ["toutes"],
            "materials": ["tablier"]
        }
        
        response = client.post(
            "/api/v1/activities/", 
            json=activity_data, 
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["slug"] == "new-test-activity"
        assert data["title"] == "New Test Activity"

    def test_update_activity(self, client, auth_headers, test_activity):
        """Test updating activity."""
        update_data = {
            "title": "Updated Test Activity",
            "summary": "Updated summary"
        }
        
        response = client.put(
            f"/api/v1/activities/{test_activity.id}",
            json=update_data,
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Test Activity"
        assert data["summary"] == "Updated summary"

    def test_delete_activity(self, client, auth_headers, test_activity):
        """Test deleting activity."""
        response = client.delete(
            f"/api/v1/activities/{test_activity.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204

    def test_get_activity_sessions(self, client, test_activity):
        """Test getting sessions for an activity."""
        response = client.get(f"/api/v1/activities/{test_activity.id}/sessions")
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_create_activity_session(self, client, auth_headers, test_activity):
        """Test creating activity session."""
        from datetime import datetime, timedelta
        
        start_date = datetime.now() + timedelta(days=7)
        end_date = start_date + timedelta(hours=2)
        
        session_data = {
            "title": "Test Session",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "location": "Test Location",
            "max_participants": 8
        }
        
        response = client.post(
            f"/api/v1/activities/{test_activity.id}/sessions",
            json=session_data,
            headers=auth_headers
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Session"
        assert data["location"] == "Test Location"