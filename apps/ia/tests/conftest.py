import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from app.models.models import User, Activity
from app.core.security import get_password_hash

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
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
def client():
    """Create test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session():
    """Create database session for testing."""
    # Create fresh tables for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("testpass"),
        full_name="Test User",
        location="Test Location",
        skills=["test_skill"],
        availability=["weekend"],
        preferences=["agri"]
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_activity(db_session):
    """Create a test activity."""
    activity = Activity(
        slug="test-activity",
        title="Test Activity",
        category="agri",
        summary="Test summary",
        duration_min=60,
        skill_tags=["test_skill"],
        seasonality=["toutes"],
        safety_level=1,
        materials=["gants"]
    )
    db_session.add(activity)
    db_session.commit()
    db_session.refresh(activity)
    return activity


@pytest.fixture
def auth_headers(client, test_user):
    """Get authentication headers for a test user."""
    response = client.post(
        "/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}