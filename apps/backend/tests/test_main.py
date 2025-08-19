import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import get_db
from models import Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert data["status"] == "healthy"

def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_register_user():
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User",
        "role": "student"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "hashed_password" not in data

def test_register_duplicate_user():
    """Test registration with duplicate username."""
    user_data = {
        "email": "test2@example.com",
        "username": "testuser",  # Same username as above
        "password": "testpassword123",
        "role": "student"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login():
    """Test user login."""
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_current_user():
    """Test getting current user profile."""
    # First login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    
    # Test getting user profile
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_list_activities():
    """Test listing activities."""
    response = client.get("/activities/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data

def test_get_activity_categories():
    """Test getting activity categories."""
    response = client.get("/activities/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    expected_categories = ["agri", "transfo", "artisanat", "nature", "social"]
    for category in expected_categories:
        assert category in categories

def test_list_locations():
    """Test listing locations."""
    response = client.get("/locations/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data

def test_unauthorized_access():
    """Test accessing protected endpoints without token."""
    response = client.get("/users/")
    assert response.status_code == 401

def test_create_location_unauthorized():
    """Test creating location without proper permissions."""
    location_data = {
        "name": "Test Farm",
        "description": "A test farm location",
        "departement": "Test Department"
    }
    
    # Try without token
    response = client.post("/locations/", json=location_data)
    assert response.status_code == 401
    
    # Try with student token
    login_data = {
        "username": "testuser",
        "password": "testpassword123"
    }
    
    login_response = client.post("/auth/login", json=login_data)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/locations/", json=location_data, headers=headers)
    assert response.status_code == 403  # Student should not have permission

@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up database after each test."""
    yield
    # Clean up test data if needed
    db = TestingSessionLocal()
    try:
        # You could add cleanup logic here
        pass
    finally:
        db.close()