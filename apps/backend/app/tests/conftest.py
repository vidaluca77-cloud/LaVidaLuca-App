import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.database import get_db, Base
from app.models.models import User, Activity
from app.core.auth import get_password_hash

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def test_client():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create test client
    client = TestClient(app)
    
    # Seed test data
    db = TestingSessionLocal()
    
    # Create test user
    test_user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        skills=["elevage", "soil"],
        availability=["weekend"],
        location="Test Location",
        preferences=["agri"]
    )
    db.add(test_user)
    
    # Create test activities
    test_activity = Activity(
        slug="test-activity",
        title="Test Activity",
        category="agri",
        summary="A test activity",
        duration_min=60,
        skill_tags=["elevage"],
        seasonality=["printemps"],
        safety_level=1,
        materials=["gants"]
    )
    db.add(test_activity)
    
    db.commit()
    db.close()
    
    yield client
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)