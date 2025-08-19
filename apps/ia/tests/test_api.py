import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import os
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("main.openai.chat.completions.create")
def test_guide(mock_openai):
    # Mock OpenAI response
    class MockResponse:
        class Choice:
            class Message:
                content = "Test answer"
            message = Message()
        choices = [Choice()]
    mock_openai.return_value = MockResponse()

    response = client.post("/guide", json={
        "question": "Test question",
        "activity_title": "Test Activity",
        "safety_level": 1,
        "duration_min": 30,
        "materials": ["test"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Activity"
    assert data["answer"] == "Test answer"

@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
@patch("main.openai.chat.completions.create")
def test_chat(mock_openai):
    # Mock OpenAI response
    class MockResponse:
        class Choice:
            class Message:
                content = "Test answer"
            message = Message()
        choices = [Choice()]
    mock_openai.return_value = MockResponse()

    response = client.post("/chat", json={
        "messages": [
            {"role": "user", "content": "Test message"}
        ]
    })
    
    assert response.status_code == 200
    assert response.json() == {"answer": "Test answer"}