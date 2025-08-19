import pytest
from src.main import app

def test_app_creation():
    """Test that the FastAPI app is created successfully"""
    assert app is not None
    assert app.title == "La Vida Luca API"
    assert app.version == "1.0.0"

def test_app_routes():
    """Test that the app has the expected routes"""
    routes = [route.path for route in app.routes]
    assert "/" in routes
    assert "/health" in routes