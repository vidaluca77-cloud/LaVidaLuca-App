import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from app.api.deps import get_db
from app.models.base import Base

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

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "LaVidaLuca" in response.json()["message"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(setup_database):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data


def test_register_duplicate_user(setup_database):
    # First registration
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    
    # Duplicate registration
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword",
            "full_name": "Test User 2"
        }
    )
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"]


def test_login_user(setup_database):
    # Register a user first
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "testpassword",
            "full_name": "Login User"
        }
    )
    
    # Test login
    response = client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "login@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_credentials(setup_database):
    response = client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


def test_get_activities():
    response = client.get("/api/v1/activities/")
    assert response.status_code == 200
    # Should return empty list since no activities in test DB
    assert isinstance(response.json(), list)


def test_get_activity_categories():
    response = client.get("/api/v1/activities/categories/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_activity_skills():
    response = client.get("/api/v1/activities/skills/")
    assert response.status_code == 200
    skills = response.json()
    assert isinstance(skills, list)
    assert "elevage" in skills
    assert "hygiene" in skills