import pytest

def test_create_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_login(client):
    # First create a user
    client.post(
        "/auth/register",
        json={
            "email": "login_test@example.com",
            "password": "testpass123",
            "full_name": "Login Test User"
        }
    )
    
    # Then try to login
    response = client.post(
        "/auth/login",
        data={
            "username": "login_test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_duplicate_email_registration(client):
    # Register first user
    client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpass123",
            "full_name": "First User"
        }
    )
    
    # Try to register with same email
    response = client.post(
        "/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "testpass456",
            "full_name": "Second User"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]