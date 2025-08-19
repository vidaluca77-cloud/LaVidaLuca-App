"""
Comprehensive test configuration and fixtures for LaVidaLuca Backend.
"""

import pytest
import tempfile
import os
from typing import Generator, Any
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import factory
from datetime import datetime, timedelta

# Import app and dependencies
import sys
sys.path.append('/home/runner/work/LaVidaLuca-App/LaVidaLuca-App/apps/backend')
from app.main import app
from app.db.database import get_db, Base
from app.models.models import User, Activity, ActivitySuggestion
from app.core.security import get_password_hash, create_access_token
from app.core.config import settings


# Test database setup - use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Factories for test data creation
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating test users."""
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user{n}")
    full_name = factory.Faker("name")
    hashed_password = factory.LazyFunction(lambda: get_password_hash("testpassword"))
    is_active = True
    is_superuser = False
    created_at = factory.LazyFunction(datetime.utcnow)


class ActivityFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating test activities."""
    class Meta:
        model = Activity
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text", max_nb_chars=200)
    category = factory.Faker("random_element", elements=("sports", "arts", "technology", "nature"))
    difficulty_level = factory.Faker("random_element", elements=("beginner", "intermediate", "advanced"))
    duration_minutes = factory.Faker("random_int", min=30, max=180)
    location = factory.Faker("city")
    equipment_needed = factory.Faker("text", max_nb_chars=100)
    learning_objectives = factory.Faker("text", max_nb_chars=150)
    is_published = True
    created_at = factory.LazyFunction(datetime.utcnow)
    creator_id = factory.SubFactory(UserFactory)


class ActivitySuggestionFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating test activity suggestions."""
    class Meta:
        model = ActivitySuggestion
        sqlalchemy_session_persistence = "commit"

    id = factory.Sequence(lambda n: n)
    suggestion_reason = factory.Faker("text", max_nb_chars=100)
    ai_generated = True
    created_at = factory.LazyFunction(datetime.utcnow)
    user_id = factory.SubFactory(UserFactory)
    activity_id = factory.SubFactory(ActivityFactory)


# Pytest fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create and tear down test database."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables
    Base.metadata.drop_all(bind=engine)
    # Clean up test database file
    try:
        os.remove("./test.db")
    except FileNotFoundError:
        pass


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Create a fresh database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Set session for factories
    UserFactory._meta.sqlalchemy_session = session
    ActivityFactory._meta.sqlalchemy_session = session
    ActivitySuggestionFactory._meta.sqlalchemy_session = session
    
    # Override the dependency
    app.dependency_overrides[get_db] = lambda: session
    
    yield session
    
    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()
    
    # Remove override
    if get_db in app.dependency_overrides:
        del app.dependency_overrides[get_db]


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client with database session."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user."""
    user = UserFactory()
    db_session.commit()
    return user


@pytest.fixture
def test_superuser(db_session: Session) -> User:
    """Create a test superuser."""
    user = UserFactory(is_superuser=True)
    db_session.commit()
    return user


@pytest.fixture
def test_activity(db_session: Session, test_user: User) -> Activity:
    """Create a test activity."""
    activity = ActivityFactory(creator_id=test_user.id)
    db_session.commit()
    return activity


@pytest.fixture
def test_activities(db_session: Session, test_user: User) -> list[Activity]:
    """Create multiple test activities."""
    activities = ActivityFactory.create_batch(5, creator_id=test_user.id)
    db_session.commit()
    return activities


@pytest.fixture
def auth_headers(test_user: User) -> dict[str, str]:
    """Create authentication headers for test user."""
    access_token = create_access_token(subject=test_user.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def superuser_auth_headers(test_superuser: User) -> dict[str, str]:
    """Create authentication headers for test superuser."""
    access_token = create_access_token(subject=test_superuser.id)
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def sample_user_data() -> dict[str, Any]:
    """Sample user data for testing."""
    return {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User",
        "is_active": True
    }


@pytest.fixture
def sample_activity_data() -> dict[str, Any]:
    """Sample activity data for testing."""
    return {
        "title": "Test Activity",
        "description": "A test activity for unit testing",
        "category": "technology",
        "difficulty_level": "beginner",
        "duration_minutes": 60,
        "location": "Online",
        "equipment_needed": "Computer, Internet",
        "learning_objectives": "Learn testing concepts",
        "is_published": True
    }


@pytest.fixture
def multiple_users(db_session: Session) -> list[User]:
    """Create multiple test users."""
    users = UserFactory.create_batch(3)
    db_session.commit()
    return users


@pytest.fixture
def expired_token() -> str:
    """Create an expired JWT token for testing."""
    return create_access_token(
        subject=1, 
        expires_delta=timedelta(minutes=-30)  # Expired 30 minutes ago
    )