"""
Pytest configuration and fixtures for backend tests.
"""

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.database.database import get_db, Base
from backend.database.models import User, Activity
from backend.auth.auth import get_password_hash, create_access_token

# Test database URL (in-memory SQLite)
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Create test session factory
TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_test_db():
    """Get test database session."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session):
    """Create a test client with test database."""
    app.dependency_overrides[get_db] = lambda: db_session
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        first_name="Test",
        last_name="User",
        skills=["python", "testing"],
        availability=["weekends"],
        location="Test City",
        bio="Test user bio",
        is_active=True,
        is_verified=True
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture
async def test_activity(db_session, test_user):
    """Create a test activity."""
    activity = Activity(
        title="Test Activity",
        category="agri",
        summary="A test activity for testing",
        description="Detailed description of test activity",
        duration_min=60,
        skill_tags=["testing", "python"],
        safety_level=2,
        materials=["laptop", "notebook"],
        location_type="indoor",
        season=["spring", "summer"],
        created_by=test_user.id
    )
    
    db_session.add(activity)
    await db_session.commit()
    await db_session.refresh(activity)
    
    return activity


@pytest.fixture
async def auth_headers(test_user):
    """Create authentication headers for test user."""
    token = create_access_token(data={"sub": test_user.id, "email": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
async def admin_user(db_session):
    """Create an admin test user."""
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        first_name="Admin",
        last_name="User",
        is_active=True,
        is_verified=True
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture
async def admin_headers(admin_user):
    """Create authentication headers for admin user."""
    token = create_access_token(data={"sub": admin_user.id, "email": admin_user.email})
    return {"Authorization": f"Bearer {token}"}


# Test data fixtures
@pytest.fixture
def sample_activity_data():
    """Sample activity creation data."""
    return {
        "title": "Organic Vegetable Gardening",
        "category": "agri",
        "summary": "Learn the basics of organic vegetable gardening",
        "description": "A comprehensive course on organic vegetable gardening techniques",
        "duration_min": 120,
        "skill_tags": ["gardening", "organic", "sustainability"],
        "safety_level": 2,
        "materials": ["seeds", "tools", "compost"],
        "location_type": "outdoor",
        "season": ["spring", "summer", "fall"]
    }


@pytest.fixture
def sample_user_data():
    """Sample user registration data."""
    return {
        "email": "newuser@example.com",
        "password": "newuserpassword",
        "first_name": "New",
        "last_name": "User",
        "skills": ["agriculture", "sustainability"],
        "availability": ["weekends", "evenings"],
        "location": "Rural France",
        "bio": "Interested in sustainable agriculture"
    }