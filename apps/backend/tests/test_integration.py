import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestAPIIntegration:
    """Integration tests for the complete API workflow."""

    async def test_complete_user_journey(self, client: AsyncClient):
        """Test the complete user journey from registration to suggestions."""
        
        # 1. Register a new user
        user_data = {
            "email": "journey@lavidaluca.fr",
            "password": "JourneyTest123!",
            "first_name": "Journey",
            "last_name": "User"
        }
        
        register_response = await client.post("/api/v1/auth/register", json=user_data)
        assert register_response.status_code == 200
        register_data = register_response.json()
        assert register_data["success"] is True
        assert register_data["data"]["email"] == user_data["email"]
        
        # 2. Login with the new user
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        login_data = login_response.json()
        assert login_data["success"] is True
        access_token = login_data["data"]["access_token"]
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        # 3. Update user profile
        profile_data = {
            "skills": ["elevage", "hygiene"],
            "availability": ["weekend"],
            "location": "Auvergne-Rhône-Alpes",
            "preferences": ["agri", "nature"]
        }
        
        profile_response = await client.put(
            "/api/v1/users/profile", 
            json=profile_data, 
            headers=headers
        )
        assert profile_response.status_code == 200
        
        # 4. Get activities catalog
        activities_response = await client.get("/api/v1/activities/")
        assert activities_response.status_code == 200
        activities_data = activities_response.json()
        assert activities_data["success"] is True
        assert len(activities_data["data"]) > 0
        
        # 5. Get personalized suggestions
        suggestions_response = await client.post(
            "/api/v1/suggestions/generate",
            json=profile_data,
            headers=headers
        )
        assert suggestions_response.status_code == 200
        suggestions_data = suggestions_response.json()
        assert suggestions_data["success"] is True
        assert len(suggestions_data["data"]) > 0
        
        # 6. Submit a contact request
        contact_data = {
            "name": "Journey User",
            "email": "journey@lavidaluca.fr",
            "subject": "Inscription activité",
            "message": "Je souhaite m'inscrire à une activité",
            "activity_id": suggestions_data["data"][0]["activity"]["id"]
        }
        
        contact_response = await client.post("/api/v1/contacts/submit", json=contact_data)
        assert contact_response.status_code == 200
        contact_data = contact_response.json()
        assert contact_data["success"] is True

    async def test_authentication_flow(self, client: AsyncClient):
        """Test complete authentication workflow."""
        
        # Test registration with duplicate email fails
        user_data = {
            "email": "duplicate@lavidaluca.fr",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        # First registration should succeed
        response1 = await client.post("/api/v1/auth/register", json=user_data)
        assert response1.status_code == 200
        
        # Second registration with same email should fail
        response2 = await client.post("/api/v1/auth/register", json=user_data)
        assert response2.status_code == 400
        
        # Test login with correct credentials
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        login_response = await client.post("/api/v1/auth/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()["data"]
        access_token = token_data["access_token"]
        
        # Test token verification
        headers = {"Authorization": f"Bearer {access_token}"}
        verify_response = await client.post("/api/v1/auth/verify-token", headers=headers)
        assert verify_response.status_code == 200
        
        # Test login with wrong password
        wrong_login_data = {
            "email": user_data["email"],
            "password": "WrongPassword"
        }
        
        wrong_login_response = await client.post("/api/v1/auth/login", json=wrong_login_data)
        assert wrong_login_response.status_code == 401

    async def test_api_error_handling(self, client: AsyncClient, auth_headers):
        """Test API error handling and validation."""
        
        # Test accessing protected endpoint without auth
        response = await client.get("/api/v1/users/profile")
        assert response.status_code == 401
        
        # Test invalid data validation
        invalid_user_data = {
            "email": "invalid-email",  # Invalid email format
            "password": "123",  # Too short password
            "first_name": "",  # Empty name
            "last_name": ""
        }
        
        register_response = await client.post("/api/v1/auth/register", json=invalid_user_data)
        assert register_response.status_code == 422  # Validation error
        
        # Test invalid JSON
        response = await client.post(
            "/api/v1/contacts/submit",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    async def test_suggestions_algorithm(self, client: AsyncClient, auth_headers):
        """Test the AI suggestions algorithm."""
        
        # Test with specific profile to verify matching logic
        profile1 = {
            "skills": ["elevage", "responsabilite"],
            "availability": ["weekend"],
            "location": "Bretagne",
            "preferences": ["agri"]
        }
        
        suggestions1_response = await client.post(
            "/api/v1/suggestions/generate",
            json=profile1,
            headers=auth_headers
        )
        assert suggestions1_response.status_code == 200
        suggestions1 = suggestions1_response.json()["data"]
        
        # Verify that suggestions are returned
        assert len(suggestions1) > 0
        assert all("score" in suggestion for suggestion in suggestions1)
        assert all("reasons" in suggestion for suggestion in suggestions1)
        
        # Test with different profile
        profile2 = {
            "skills": ["creativite", "patience"],
            "availability": ["semaine"],
            "location": "Provence",
            "preferences": ["artisanat", "social"]
        }
        
        suggestions2_response = await client.post(
            "/api/v1/suggestions/generate",
            json=profile2,
            headers=auth_headers
        )
        assert suggestions2_response.status_code == 200
        suggestions2 = suggestions2_response.json()["data"]
        
        # Verify different profiles get different suggestions
        assert len(suggestions2) > 0
        
        # The top suggestions should be different for different profiles
        top_suggestion1 = suggestions1[0]["activity"]["id"]
        top_suggestion2 = suggestions2[0]["activity"]["id"]
        
        # They might be the same, but scores should be different
        if top_suggestion1 == top_suggestion2:
            assert suggestions1[0]["score"] != suggestions2[0]["score"]

    async def test_performance_endpoints(self, client: AsyncClient):
        """Test API performance under load."""
        import asyncio
        
        # Test concurrent requests to activities endpoint
        async def get_activities():
            response = await client.get("/api/v1/activities/")
            return response.status_code
        
        # Run 10 concurrent requests
        tasks = [get_activities() for _ in range(10)]
        results = await asyncio.gather(*tasks)
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        
        # Test health check endpoint
        health_response = await client.get("/health")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["status"] == "healthy"