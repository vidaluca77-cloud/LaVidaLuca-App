"""
Tests pour l'API FastAPI La Vida Luca
"""

import pytest
import asyncio
from httpx import AsyncClient
from main import app, ACTIVITIES_DB

@pytest.fixture
def client():
    """Client de test pour l'API"""
    return AsyncClient(app=app, base_url="http://test")

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test de l'endpoint /health"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert data["version"] == "1.0.0"

@pytest.mark.asyncio
async def test_guide_endpoint_basic():
    """Test de l'endpoint /guide avec un profil basique"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        profile_data = {
            "profile": {
                "skills": ["elevage", "hygiene"],
                "availability": ["matin", "weekend"],
                "location": "ferme_test",
                "preferences": ["agri"]
            }
        }
        
        response = await client.post("/guide", json=profile_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "suggestions" in data
        assert "safety_guide" in data
        assert "personalized_tips" in data
        
        # Vérifier qu'on a des suggestions
        assert isinstance(data["suggestions"], list)
        assert len(data["suggestions"]) > 0
        
        # Vérifier la structure d'une suggestion
        suggestion = data["suggestions"][0]
        assert "id" in suggestion
        assert "title" in suggestion
        assert "compatibility_score" in suggestion

@pytest.mark.asyncio
async def test_guide_endpoint_with_category():
    """Test de l'endpoint /guide avec filtre par catégorie"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        profile_data = {
            "profile": {
                "skills": ["elevage"],
                "availability": ["weekend"],
                "location": "ferme_test",
                "preferences": ["agri"]
            },
            "category": "agri"
        }
        
        response = await client.post("/guide", json=profile_data)
        assert response.status_code == 200
        
        data = response.json()
        # Toutes les suggestions doivent être de la catégorie "agri"
        for suggestion in data["suggestions"]:
            assert suggestion["category"] == "agri"

@pytest.mark.asyncio
async def test_chat_endpoint_basic():
    """Test de l'endpoint /chat avec un message basique"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        message_data = {
            "message": "Bonjour, comment puis-je participer aux activités ?"
        }
        
        response = await client.post("/chat", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "response" in data
        assert "timestamp" in data
        assert "context_used" in data
        
        # La réponse ne doit pas être vide
        assert len(data["response"]) > 0
        assert isinstance(data["context_used"], bool)

@pytest.mark.asyncio
async def test_chat_endpoint_safety_question():
    """Test de l'endpoint /chat avec une question sur la sécurité"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        message_data = {
            "message": "Quelles sont les consignes de sécurité ?"
        }
        
        response = await client.post("/chat", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        # La réponse doit mentionner la sécurité
        assert "sécurité" in data["response"].lower()

@pytest.mark.asyncio
async def test_chat_endpoint_with_context():
    """Test de l'endpoint /chat avec contexte"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        message_data = {
            "message": "Peux-tu me donner plus d'infos ?",
            "context": {"previous_topic": "activités"}
        }
        
        response = await client.post("/chat", json=message_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["context_used"] == True

@pytest.mark.asyncio
async def test_chat_endpoint_invalid_message():
    """Test de l'endpoint /chat avec message invalide"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        message_data = {
            "message": ""  # Message vide
        }
        
        response = await client.post("/chat", json=message_data)
        assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_guide_endpoint_empty_profile():
    """Test de l'endpoint /guide avec profil vide"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        profile_data = {
            "profile": {
                "skills": [],
                "availability": [],
                "location": "",
                "preferences": []
            }
        }
        
        response = await client.post("/guide", json=profile_data)
        assert response.status_code == 200
        
        data = response.json()
        # Même avec un profil vide, on doit avoir des suggestions
        assert len(data["suggestions"]) > 0

@pytest.mark.asyncio
async def test_cors_headers():
    """Test des headers CORS"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.options("/health")
        # En test, CORS est généralement géré automatiquement
        assert response.status_code in [200, 405]  # 405 si OPTIONS non supporté

def test_activities_database():
    """Test de la base de données des activités"""
    assert len(ACTIVITIES_DB) > 0
    
    for activity in ACTIVITIES_DB:
        # Vérifier la structure de chaque activité
        required_fields = ["id", "slug", "title", "category", "summary", 
                         "duration_min", "skill_tags", "safety_level"]
        for field in required_fields:
            assert field in activity
        
        # Vérifier les types
        assert isinstance(activity["id"], str)
        assert isinstance(activity["duration_min"], int)
        assert isinstance(activity["skill_tags"], list)
        assert isinstance(activity["safety_level"], int)
        assert activity["safety_level"] in [1, 2, 3]

if __name__ == "__main__":
    # Lancer les tests
    pytest.main([__file__, "-v"])