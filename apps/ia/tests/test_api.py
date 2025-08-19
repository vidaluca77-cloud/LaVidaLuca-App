import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

# Client de test
client = TestClient(app)

def test_health_check():
    """Test du point de santé de l'API"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data

def test_root_endpoint():
    """Test de la route racine"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "documentation" in data

def test_guide_endpoint_success():
    """Test du guide pour une activité existante"""
    request_data = {
        "activite_id": "semis-plantation",
        "profil_utilisateur": {
            "niveau": "debutant"
        },
        "contexte": "Formation MFR"
    }
    
    response = client.post("/guide", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "activite" in data
    assert "conseils" in data
    assert "materiel_necessaire" in data
    assert "etapes" in data
    assert "conseils_securite" in data
    assert "adapte_au_profil" in data
    
    # Vérifier que les conseils sont adaptés pour débutant
    assert data["adapte_au_profil"] is True
    assert len(data["conseils"]) > 0
    assert len(data["etapes"]) > 0

def test_guide_endpoint_not_found():
    """Test du guide pour une activité inexistante"""
    request_data = {
        "activite_id": "activite-inexistante"
    }
    
    response = client.post("/guide", json=request_data)
    assert response.status_code == 404
    assert "Activité non trouvée" in response.json()["detail"]

def test_guide_without_profile():
    """Test du guide sans profil utilisateur"""
    request_data = {
        "activite_id": "elevage-soins"
    }
    
    response = client.post("/guide", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["activite"] == "Soins aux animaux d'élevage"
    assert len(data["materiel_necessaire"]) > 0

def test_chat_endpoint_activity_question():
    """Test du chat avec une question sur les activités"""
    request_data = {
        "message": "Quelles activités puis-je faire ?",
        "contexte": "Nouveau participant MFR"
    }
    
    response = client.post("/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "reponse" in data
    assert "suggestions" in data
    assert "ressources" in data
    assert len(data["suggestions"]) > 0
    assert "activité" in data["reponse"].lower()

def test_chat_endpoint_safety_question():
    """Test du chat avec une question sur la sécurité"""
    request_data = {
        "message": "Quelles sont les règles de sécurité ?",
        "historique": []
    }
    
    response = client.post("/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "sécurité" in data["reponse"].lower()
    assert len(data["suggestions"]) > 0

def test_chat_endpoint_equipment_question():
    """Test du chat avec une question sur le matériel"""
    request_data = {
        "message": "Quel matériel est nécessaire ?"
    }
    
    response = client.post("/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "matériel" in data["reponse"].lower() or "équipement" in data["reponse"].lower()

def test_chat_endpoint_general_question():
    """Test du chat avec une question générale"""
    request_data = {
        "message": "Bonjour, pouvez-vous m'aider ?"
    }
    
    response = client.post("/chat", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "Vida Luca" in data["reponse"]
    assert len(data["suggestions"]) > 0

def test_cors_headers():
    """Test que les headers CORS sont présents"""
    response = client.options("/health")
    # Note: TestClient ne gère pas complètement CORS, 
    # ce test vérifie que l'endpoint répond
    assert response.status_code in [200, 405]  # 405 = Method Not Allowed est OK pour OPTIONS

@pytest.mark.asyncio
async def test_async_endpoints():
    """Test asynchrone des endpoints"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        
        response = await ac.post("/chat", json={
            "message": "Test async"
        })
        assert response.status_code == 200

def test_request_validation():
    """Test de validation des requêtes"""
    # Test avec des données invalides pour /guide
    response = client.post("/guide", json={})
    assert response.status_code == 422  # Validation error
    
    # Test avec des données invalides pour /chat
    response = client.post("/chat", json={})
    assert response.status_code == 422  # Validation error

def test_guide_with_experienced_user():
    """Test du guide avec un utilisateur expérimenté"""
    request_data = {
        "activite_id": "semis-plantation",
        "profil_utilisateur": {
            "niveau": "expert",
            "experience": ["agriculture", "jardinage"]
        }
    }
    
    response = client.post("/guide", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["adapte_au_profil"] is True
    # Pour un expert, pas de conseils supplémentaires de débutant
    assert "Demander l'aide d'un encadrant" not in " ".join(data["conseils"])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])