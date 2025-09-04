"""
Test configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.models.models import Base
from app.db.database import get_db
from app.core.security import get_current_active_user

# Test database URL
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

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test"""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency overrides"""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "testpassword123",
        "skills": ["elevage", "hygiene"],
        "availability": ["weekend", "matin"],
        "preferences": ["agri", "nature"]
    }

@pytest.fixture
def test_activity_data():
    """Sample activity data for testing"""
    return {
        "slug": "test-activity",
        "title": "Test Activity",
        "category": "agri",
        "summary": "A test activity for unit tests",
        "duration_min": 60,
        "skill_tags": ["test", "demo"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["gants"]
    }