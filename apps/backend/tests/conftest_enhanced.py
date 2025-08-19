import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db_session, Base
from config import settings

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

# Create test session factory
TestAsyncSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_test_db():
    """Override database dependency for testing."""
    async with TestAsyncSessionLocal() as session:
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


@pytest.fixture(scope="session")
async def test_db():
    """Create test database tables."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client(test_db):
    """Create test client with database override."""
    app.dependency_overrides[get_db_session] = get_test_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_session(test_db):
    """Create test database session."""
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture
async def auth_headers(client: AsyncClient):
    """Create authentication headers for testing."""
    # Register test user
    user_data = {
        "email": "test@lavidaluca.fr",
        "password": "TestPassword123!",
        "first_name": "Test",
        "last_name": "User"
    }
    
    register_response = await client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # Login test user
    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    
    login_response = await client.post("/api/v1/auth/login", json=login_data)
    assert login_response.status_code == 200
    
    token_data = login_response.json()["data"]
    access_token = token_data["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def sample_user_profile():
    """Sample user profile for testing."""
    return {
        "skills": ["elevage", "hygiene", "soins_animaux"],
        "availability": ["weekend", "matin"],
        "location": "Île-de-France",
        "preferences": ["agri", "nature"]
    }


@pytest.fixture
def sample_activity():
    """Sample activity for testing."""
    return {
        "title": "Test Activity",
        "slug": "test-activity",
        "category": "agri",
        "summary": "A test activity for learning",
        "duration_min": 60,
        "skill_tags": ["elevage", "responsabilite"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["gants", "bottes"]
    }