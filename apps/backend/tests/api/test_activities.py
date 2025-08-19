"""Test activities API endpoints."""

from fastapi.testclient import TestClient
from uuid import uuid4

from src.core.security import get_password_hash
from src.models.user import User, UserRole
from src.models.location import Location
from src.models.activity import Activity


def create_test_user(db, role=UserRole.STUDENT, email="test@example.com"):
    """Create a test user."""
    hashed_password = get_password_hash("testpassword")
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name="Test User",
        role=role,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_test_location(db):
    """Create a test location."""
    location = Location(
        name="Test Farm",
        address="123 Test Street",
        city="Test City",
        postal_code="12345",
        country="France"
    )
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def create_test_activity(db, location_id):
    """Create a test activity."""
    activity = Activity(
        title="Test Activity",
        slug="test-activity",
        description="A test activity for testing purposes",
        category="agri",
        duration_min=60,
        max_participants=10,
        difficulty_level=2,
        materials=["gants", "bottes"],
        skill_tags=["test", "farming"],
        seasonality=["printemps"],
        safety_level=1,
        location_id=location_id,
        is_active=True
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def get_auth_headers(client: TestClient, email: str, password: str):
    """Get authentication headers for testing."""
    response = client.post(
        "/api/v1/auth/login/json",
        json={"email": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_activities(client: TestClient, db):
    """Test getting activities."""
    # Create test data
    user = create_test_user(db)
    location = create_test_location(db)
    activity = create_test_activity(db, location.id)
    
    # Get auth headers
    headers = get_auth_headers(client, user.email, "testpassword")
    
    # Test getting activities
    response = client.get("/api/v1/activities/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Test Activity"


def test_create_activity_as_instructor(client: TestClient, db):
    """Test creating activity as instructor."""
    # Create test data
    instructor = create_test_user(db, role=UserRole.INSTRUCTOR, email="instructor@test.com")
    location = create_test_location(db)
    
    # Get auth headers
    headers = get_auth_headers(client, instructor.email, "testpassword")
    
    # Test creating activity
    activity_data = {
        "title": "New Activity",
        "slug": "new-activity",
        "description": "A new test activity",
        "category": "agri",
        "duration_min": 90,
        "max_participants": 15,
        "difficulty_level": 3,
        "materials": ["tools"],
        "skill_tags": ["farming"],
        "seasonality": ["summer"],
        "safety_level": 2,
        "location_id": str(location.id)
    }
    
    response = client.post("/api/v1/activities/", json=activity_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Activity"
    assert data["slug"] == "new-activity"


def test_create_activity_as_student_fails(client: TestClient, db):
    """Test that students cannot create activities."""
    # Create test data
    student = create_test_user(db)
    location = create_test_location(db)
    
    # Get auth headers
    headers = get_auth_headers(client, student.email, "testpassword")
    
    # Test creating activity (should fail)
    activity_data = {
        "title": "Student Activity",
        "slug": "student-activity",
        "description": "Should not be allowed",
        "category": "agri",
        "duration_min": 60,
        "difficulty_level": 1,
        "safety_level": 1
    }
    
    response = client.post("/api/v1/activities/", json=activity_data, headers=headers)
    assert response.status_code == 403


def test_get_activity_by_slug(client: TestClient, db):
    """Test getting activity by slug."""
    # Create test data
    user = create_test_user(db)
    location = create_test_location(db)
    activity = create_test_activity(db, location.id)
    
    # Get auth headers
    headers = get_auth_headers(client, user.email, "testpassword")
    
    # Test getting activity by slug
    response = client.get(f"/api/v1/activities/slug/{activity.slug}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["slug"] == activity.slug
    assert data["title"] == activity.title


def test_search_activities(client: TestClient, db):
    """Test searching activities."""
    # Create test data
    user = create_test_user(db)
    location = create_test_location(db)
    activity = create_test_activity(db, location.id)
    
    # Get auth headers
    headers = get_auth_headers(client, user.email, "testpassword")
    
    # Test search
    response = client.get("/api/v1/activities/search/?q=Test", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1