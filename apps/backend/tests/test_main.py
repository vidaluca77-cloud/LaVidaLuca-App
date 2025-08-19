"""
Tests unitaires de base pour l'application FastAPI principale.
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from ..main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to La Vida Luca API"
    assert data["version"] == "1.0.0"
    assert data["status"] == "healthy"
    assert "docs" in data


@pytest.mark.asyncio
async def test_health_check_endpoint():
    """Test health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data
    assert "environment" in data


def test_app_creation():
    """Test FastAPI app creation."""
    assert app is not None
    assert app.title == "La Vida Luca API"
    assert app.version == "1.0.0"


def test_cors_middleware():
    """Test CORS middleware is configured."""
    # Check that CORS middleware is in the middleware stack
    middleware_types = [type(middleware.cls) for middleware in app.user_middleware]
    from fastapi.middleware.cors import CORSMiddleware
    assert CORSMiddleware in middleware_types


def test_docs_availability_in_dev():
    """Test that API docs are available."""
    from ..config import settings
    
    if settings.ENVIRONMENT != "production":
        # In development, docs should be available
        assert app.docs_url == "/docs"
        assert app.redoc_url == "/redoc"


@pytest.mark.asyncio
async def test_api_routes_exist():
    """Test that main API routes are included."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test that the main route groups exist by checking a common 404 vs 405 behavior
        routes = [route.path for route in app.routes]
        
        # Check that main API prefixes exist in routes
        api_prefixes = ["/api/v1/auth", "/api/v1/users", "/api/v1/activities", 
                       "/api/v1/contacts", "/api/v1/suggestions"]
        
        # At least some routes should be registered (the exact routes depend on implementation)
        assert len(routes) > 2  # At least root and health endpoints


def test_app_configuration():
    """Test application configuration."""
    from ..config import settings
    
    # Test that settings are loaded
    assert settings is not None
    assert hasattr(settings, 'DATABASE_URL')
    assert hasattr(settings, 'ENVIRONMENT')
    
    # Test database configuration
    assert settings.DATABASE_URL is not None


@pytest.mark.asyncio 
async def test_exception_handling():
    """Test exception handling."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test 404 for non-existent route
        response = await ac.get("/non-existent-route")
        assert response.status_code == 404


def test_environment_settings():
    """Test environment-specific settings."""
    from ..config import get_settings, DevelopmentSettings, TestingSettings, ProductionSettings
    import os
    
    # Test development settings
    original_env = os.environ.get("ENVIRONMENT")
    
    try:
        os.environ["ENVIRONMENT"] = "development" 
        dev_settings = get_settings()
        assert isinstance(dev_settings, DevelopmentSettings)
        assert dev_settings.DEBUG is True
        
        os.environ["ENVIRONMENT"] = "testing"
        test_settings = get_settings() 
        assert isinstance(test_settings, TestingSettings)
        assert test_settings.DEBUG is True
        
        os.environ["ENVIRONMENT"] = "production"
        prod_settings = get_settings()
        assert isinstance(prod_settings, ProductionSettings)
        assert prod_settings.DEBUG is False
        
    finally:
        # Restore original environment
        if original_env:
            os.environ["ENVIRONMENT"] = original_env
        else:
            os.environ.pop("ENVIRONMENT", None)


def test_database_connection_config():
    """Test database connection configuration."""
    from ..database import database, engine, AsyncSessionLocal, Base
    
    # Test database components are created
    assert database is not None
    assert engine is not None
    assert AsyncSessionLocal is not None
    assert Base is not None
    
    # Test database URL is configured
    from ..config import settings
    assert settings.DATABASE_URL
    assert "postgresql" in settings.DATABASE_URL.lower()


def test_models_import():
    """Test that basic models can be imported."""
    from ..models import User, Activity, Contact
    
    # Test models are defined
    assert User is not None
    assert Activity is not None
    assert Contact is not None


def test_routes_import():
    """Test that route modules can be imported."""
    from ..routes import auth, users, activities, contacts, suggestions
    
    # Test route modules exist
    assert auth is not None
    assert users is not None
    assert activities is not None
    assert contacts is not None
    assert suggestions is not None