"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.db.base import Base
from src.db.session import get_db
from src.core.config import settings

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "confirm_password": "testpassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "student"
    }


@pytest.fixture
def sample_activity_data():
    """Sample activity data for testing."""
    return {
        "title": "Test Activity",
        "category": "agri",
        "summary": "A test activity for learning",
        "description": "Detailed description of the test activity",
        "duration_min": 60,
        "difficulty_level": 2,
        "safety_level": 1,
        "min_participants": 1,
        "max_participants": 10,
        "skill_tags": ["gardening", "basics"],
        "materials": ["shovel", "seeds"],
        "location_type": "outdoor",
        "instructions": "Follow these steps...",
        "learning_objectives": ["Learn basic gardening", "Understand soil preparation"]
    }


@pytest.fixture
def auth_headers(client, sample_user_data):
    """Create authenticated user and return authorization headers."""
    # Register user
    response = client.post("/api/v1/auth/register", json=sample_user_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}