"""
Test configuration and fixtures
"""
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.models.models import User, Activity, UserProfile
from app.core.security import get_password_hash

# Test database URL (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the database dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.fixture
def test_user(db):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_activities(db):
    """Create test activities."""
    activities = [
        Activity(
            slug="test-activity-1",
            title="Test Activity 1",
            category="agri",
            summary="Test agriculture activity",
            duration_min=60,
            skill_tags=["elevage", "responsabilite"],
            seasonality=["toutes"],
            safety_level=1,
            materials=["gants"]
        ),
        Activity(
            slug="test-activity-2",
            title="Test Activity 2",
            category="transfo",
            summary="Test transformation activity",
            duration_min=90,
            skill_tags=["hygiene", "precision"],
            seasonality=["toutes"],
            safety_level=2,
            materials=["tablier"]
        )
    ]
    
    for activity in activities:
        db.add(activity)
    db.commit()
    
    for activity in activities:
        db.refresh(activity)
    
    return activities


@pytest.fixture
def test_user_profile(db, test_user):
    """Create a test user profile."""
    profile = UserProfile(
        user_id=test_user.id,
        skills=["elevage", "hygiene"],
        preferences=["agri", "transfo"],
        availability=["weekend", "semaine"],
        location="Test Location",
        experience_level="debutant"
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}