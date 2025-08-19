import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import get_db, Base
from app.core.config import settings

# Create test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def client():
    """Create test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Automatically set up test database for each test."""
    # Create tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after each test
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user_data():
    """Test user data."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123",
        "first_name": "Test",
        "last_name": "User",
        "role": "student"
    }


@pytest.fixture
def test_activity_data():
    """Test activity data."""
    return {
        "title": "Test Activity",
        "description": "A test agricultural activity",
        "category": "agriculture",
        "level": "debutant",
        "duration_hours": 2,
        "max_participants": 10,
        "location": "Test Farm",
        "materials_needed": "Tools, seeds",
        "learning_objectives": "Learn basic farming",
        "prerequisites": "None"
    }