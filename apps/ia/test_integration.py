import pytest
import asyncio
import httpx
import os

# Integration tests that test the full system
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

@pytest.mark.asyncio
async def test_api_health():
    """Test that the API is responding and healthy"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

@pytest.mark.asyncio
async def test_full_workflow():
    """Test a complete user workflow"""
    async with httpx.AsyncClient() as client:
        # 1. Get activities
        activities_response = await client.get(f"{BASE_URL}/activities")
        assert activities_response.status_code == 200
        activities = activities_response.json()
        assert len(activities) > 0
        
        # 2. Get suggestions based on profile
        profile = {
            "skills": ["patience", "observation"],
            "availability": ["weekend"],
            "location": "test-location",
            "preferences": ["agri"]
        }
        
        suggestions_response = await client.post(
            f"{BASE_URL}/activities/suggestions",
            json=profile
        )
        assert suggestions_response.status_code == 200
        suggestions = suggestions_response.json()
        assert len(suggestions) > 0
        
        # 3. Submit contact form
        contact_data = {
            "name": "Integration Test User",
            "email": "integration@test.com",
            "subject": "Test Integration",
            "message": "This is an integration test",
            "type": "general"
        }
        
        contact_response = await client.post(
            f"{BASE_URL}/contact",
            json=contact_data
        )
        assert contact_response.status_code == 200
        contact_result = contact_response.json()
        assert contact_result["success"] is True

@pytest.mark.asyncio
async def test_authentication_flow():
    """Test the complete authentication flow"""
    async with httpx.AsyncClient() as client:
        # 1. Try to access protected route without token
        protected_response = await client.get(f"{BASE_URL}/protected")
        assert protected_response.status_code == 403
        
        # 2. Get authentication token
        token_response = await client.post(
            f"{BASE_URL}/auth/token",
            params={"username": "demo", "password": "demo"}
        )
        assert token_response.status_code == 200
        token_data = token_response.json()
        token = token_data["access_token"]
        
        # 3. Access protected route with token
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = await client.get(
            f"{BASE_URL}/protected",
            headers=headers
        )
        assert protected_response.status_code == 200
        protected_data = protected_response.json()
        assert "message" in protected_data

@pytest.mark.asyncio
async def test_cors_configuration():
    """Test that CORS is properly configured"""
    async with httpx.AsyncClient() as client:
        # Test preflight request
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = await client.options(
            f"{BASE_URL}/activities",
            headers=headers
        )
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_error_handling():
    """Test that errors are handled gracefully"""
    async with httpx.AsyncClient() as client:
        # Test invalid endpoint
        response = await client.get(f"{BASE_URL}/nonexistent")
        assert response.status_code == 404
        
        # Test invalid JSON
        response = await client.post(
            f"{BASE_URL}/contact",
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

@pytest.mark.asyncio 
async def test_frontend_backend_connection():
    """Test that frontend can connect to backend"""
    async with httpx.AsyncClient() as client:
        # Test that frontend pages are accessible
        try:
            frontend_response = await client.get(FRONTEND_URL)
            # If frontend is running, it should respond
            assert frontend_response.status_code == 200
        except httpx.ConnectError:
            # Frontend might not be running in all test environments
            pytest.skip("Frontend not available for testing")
        
        # Test API endpoint from frontend perspective
        api_response = await client.get(f"{BASE_URL}/activities")
        assert api_response.status_code == 200