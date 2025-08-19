import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.core.database import get_db, Base
from app.core.models import User, UserProfile, Activity
from app.schemas.schemas import UserCreate, UserProfileCreate, ActivityCreate
from app.services.user_service import UserService
from app.services.activity_service import ActivityService

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
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
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user_service = UserService(db_session)
    user_create = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpassword123",
        first_name="Test",
        last_name="User",
        is_mfr_student=False
    )
    return user_service.create_user(user_create)

@pytest.fixture
def test_mfr_user(db_session):
    """Create a test MFR student user."""
    user_service = UserService(db_session)
    user_create = UserCreate(
        email="mfr@example.com",
        username="mfruser",
        password="testpassword123",
        first_name="MFR",
        last_name="Student",
        is_mfr_student=True
    )
    return user_service.create_user(user_create)

@pytest.fixture
def test_activity(db_session):
    """Create a test activity."""
    activity_service = ActivityService(db_session)
    activity_create = ActivityCreate(
        slug="test-activity",
        title="Test Activity",
        category="agri",
        summary="A test activity for agriculture",
        duration_min=60,
        safety_level=1,
        skill_tags=["elevage", "responsabilite"],
        seasonality=["toutes"],
        materials=["gants"]
    )
    return activity_service.create_activity(activity_create)

@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "testuser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mfr_auth_headers(client, test_mfr_user):
    """Get authentication headers for MFR user."""
    response = client.post(
        "/api/v1/auth/login",
        json={"username_or_email": "mfruser", "password": "testpassword123"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}