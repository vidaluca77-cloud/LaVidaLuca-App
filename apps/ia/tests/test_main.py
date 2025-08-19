import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from main import app

# Use SQLite for testing
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


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "LaVidaLuca" in data["message"]


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "LaVidaLuca API"


def test_register_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword",
        "full_name": "Test User",
        "skills": ["agriculture"],
        "availability": ["weekend"],
        "location": "Test Location",
        "preferences": ["agri"]
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data


def test_login_user(client):
    # First register a user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    }
    
    client.post("/auth/register", json=user_data)
    
    # Then login
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_create_activity(client):
    # First register and login a user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    }
    
    client.post("/auth/register", json=user_data)
    
    login_response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpassword"
    })
    token = login_response.json()["access_token"]
    
    # Create activity
    activity_data = {
        "slug": "test-activity",
        "title": "Test Activity",
        "category": "agri",
        "summary": "A test activity",
        "duration_min": 60,
        "skill_tags": ["test"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["test_material"]
    }
    
    response = client.post(
        "/activities/",
        json=activity_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == activity_data["title"]
    assert data["slug"] == activity_data["slug"]


def test_get_activities(client):
    response = client.get("/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)