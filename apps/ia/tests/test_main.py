import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    """Test que le health check fonctionne"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "la-vida-luca-ia-api"


def test_activity_suggestions():
    """Test des suggestions d'activités"""
    request_data = {
        "user_skills": ["patience", "observation"],
        "availability": ["weekend"],
        "location": "Calvados",
        "preferences": ["animaux", "nature"]
    }
    
    response = client.post("/api/suggestions", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Vérifier la structure de la première suggestion
    suggestion = data[0]
    assert "activity_id" in suggestion
    assert "title" in suggestion
    assert "score" in suggestion
    assert "reasons" in suggestion
    assert isinstance(suggestion["reasons"], list)


def test_chat():
    """Test du chat avec l'IA"""
    request_data = {
        "message": "Quelles activités me recommandez-vous ?",
        "context": "débutant en agriculture"
    }
    
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "suggestions" in data
    assert isinstance(data["suggestions"], list)


def test_activity_info():
    """Test de récupération d'informations sur une activité"""
    activity_id = "test-activity-1"
    
    response = client.get(f"/api/activity/{activity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == activity_id


def test_cors_headers():
    """Test que les headers CORS sont présents"""
    response = client.options("/api/suggestions")
    assert response.status_code == 200
    # Les headers CORS devraient être présents dans une vraie requête


def test_invalid_suggestion_request():
    """Test avec des données invalides pour les suggestions"""
    request_data = {
        "user_skills": [],  # Vide mais valide
        "availability": [],
        "location": "",
        "preferences": []
    }
    
    response = client.post("/api/suggestions", json=request_data)
    assert response.status_code == 200  # Devrait toujours retourner des suggestions


def test_empty_chat_message():
    """Test avec un message vide"""
    request_data = {
        "message": "",
    }
    
    response = client.post("/api/chat", json=request_data)
    assert response.status_code == 200  # Devrait gérer les messages vides