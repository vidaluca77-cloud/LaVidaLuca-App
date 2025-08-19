import pytest

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "La Vida Luca API is running"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_activities_without_auth(client):
    response = client.get("/activities/")
    assert response.status_code == 401


def test_create_activity_without_auth(client):
    response = client.post(
        "/activities/",
        json={
            "title": "Test Activity",
            "description": "Test Description",
            "duration": 30,
            "category": "test"
        }
    )
    assert response.status_code == 401


def test_activities_with_auth(client):
    # First register and login to get token
    register_response = client.post(
        "/auth/register",
        json={
            "email": "activity_user@example.com",
            "password": "testpass123",
            "full_name": "Activity Test User"
        }
    )
    assert register_response.status_code == 200
    
    login_response = client.post(
        "/auth/login",
        data={
            "username": "activity_user@example.com",
            "password": "testpass123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    # Test creating an activity
    create_response = client.post(
        "/activities/",
        json={
            "title": "Test Activity",
            "description": "Test Description",
            "duration": 30,
            "category": "test"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert create_response.status_code == 200
    activity_data = create_response.json()
    assert activity_data["title"] == "Test Activity"
    assert activity_data["duration"] == 30
    
    # Test getting activities
    get_response = client.get(
        "/activities/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 200
    activities = get_response.json()
    assert len(activities) >= 1
    assert activities[0]["title"] == "Test Activity"