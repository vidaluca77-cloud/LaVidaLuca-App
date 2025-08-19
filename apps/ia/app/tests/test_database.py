import pytest
from sqlalchemy.orm import Session
from app.crud.crud import create_user, get_user_by_username, authenticate_user, create_activity, get_activities
from app.schemas.schemas import UserCreate, ActivityCreate
from app.core.security import get_password_hash

def test_create_user(db_session: Session):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="testpassword123"
    )
    user = create_user(db_session, user_data)
    
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.full_name == "Test User"
    assert user.id is not None
    assert user.hashed_password != "testpassword123"  # Should be hashed

def test_get_user_by_username(db_session: Session):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="testpassword123"
    )
    created_user = create_user(db_session, user_data)
    
    found_user = get_user_by_username(db_session, "testuser")
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.username == "testuser"

def test_authenticate_user(db_session: Session):
    user_data = UserCreate(
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        password="testpassword123"
    )
    create_user(db_session, user_data)
    
    # Test successful authentication
    authenticated_user = authenticate_user(db_session, "testuser", "testpassword123")
    assert authenticated_user is not None
    assert authenticated_user.username == "testuser"
    
    # Test failed authentication
    failed_auth = authenticate_user(db_session, "testuser", "wrongpassword")
    assert failed_auth is None

def test_create_activity(db_session: Session):
    activity_data = ActivityCreate(
        slug="test-activity",
        title="Test Activity",
        category="agri",
        summary="A test activity for agriculture",
        description="Detailed description",
        duration_min=90,
        skill_tags=["soil", "plants"],
        seasonality=["spring", "summer"],
        safety_level=1,
        materials=["gloves", "boots"]
    )
    
    activity = create_activity(db_session, activity_data)
    assert activity.slug == "test-activity"
    assert activity.title == "Test Activity"
    assert activity.category == "agri"
    assert activity.id is not None

def test_get_activities(db_session: Session):
    # Create test activities
    activity1 = ActivityCreate(
        slug="activity-1",
        title="Activity 1",
        category="agri",
        summary="Agriculture activity",
        duration_min=60,
        skill_tags=["soil"],
        seasonality=["spring"],
        safety_level=1,
        materials=["gloves"]
    )
    
    activity2 = ActivityCreate(
        slug="activity-2",
        title="Activity 2",
        category="transfo",
        summary="Transformation activity",
        duration_min=90,
        skill_tags=["hygiene"],
        seasonality=["summer"],
        safety_level=1,
        materials=["apron"]
    )
    
    create_activity(db_session, activity1)
    create_activity(db_session, activity2)
    
    # Test getting all activities
    all_activities = get_activities(db_session)
    assert len(all_activities) == 2
    
    # Test filtering by category
    agri_activities = get_activities(db_session, category="agri")
    assert len(agri_activities) == 1
    assert agri_activities[0].category == "agri"