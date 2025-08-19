from fastapi.testclient import TestClient
from unittest import mock
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@mock.patch("openai.OpenAI")
def test_guide(mock_openai):
    mock_openai.return_value.chat.completions.create.return_value.choices = [
        mock.Mock(message=mock.Mock(content="Test response"))
    ]
    
    response = client.post(
        "/guide",
        json={
            "question": "test question",
            "activity_title": "Test Activity",
            "safety_level": 1,
            "duration_min": 30,
            "materials": ["test"]
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Activity"
    assert data["answer"] == "Test response"

@mock.patch("openai.OpenAI")
def test_chat(mock_openai):
    mock_openai.return_value.chat.completions.create.return_value.choices = [
        mock.Mock(message=mock.Mock(content="Test response"))
    ]
    
    response = client.post(
        "/chat",
        json={
            "messages": [
                {"role": "user", "content": "test"}
            ]
        }
    )
    
    assert response.status_code == 200
    assert response.json() == {"answer": "Test response"}