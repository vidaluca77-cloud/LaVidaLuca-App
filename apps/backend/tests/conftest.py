"""
Test configuration and fixtures for La Vida Luca backend.
"""

import pytest
import asyncio
import sys
import os
from httpx import AsyncClient

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app_simple import app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client():
    """Create a test client for the simple app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
    }


@pytest.fixture
def sample_guide_question():
    """Sample guide question for testing."""
    return {"question": "Comment améliorer un sol argileux compact ?"}
