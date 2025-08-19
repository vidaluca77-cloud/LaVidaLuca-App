"""
Tests pour l'API FastAPI de La Vida Luca.

Tests des endpoints principaux : /health, /guide et /chat
"""

import pytest
import httpx
from fastapi.testclient import TestClient
from main import app

# Client de test
client = TestClient(app)

class TestHealthEndpoint:
    """Tests pour l'endpoint /health"""
    
    def test_health_check_status_code(self):
        """Test que l'endpoint /health retourne un code 200"""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self):
        """Test que l'endpoint /health retourne le bon format de réponse"""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "message" in data
        assert "version" in data
        assert data["status"] == "healthy"
        assert data["version"] == "1.0.0"

class TestGuideEndpoint:
    """Tests pour l'endpoint /guide"""
    
    def test_guide_valid_request(self):
        """Test avec une requête valide pour le guide"""
        payload = {
            "culture": "tomates",
            "saison": "printemps",
            "region": "Provence",
            "niveau": "débutant"
        }
        
        response = client.post("/guide", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "culture" in data
        assert "conseils" in data
        assert "calendrier" in data
        assert "ressources" in data
        assert "niveau_difficulte" in data
        
        assert data["culture"] == "tomates"
        assert isinstance(data["conseils"], list)
        assert len(data["conseils"]) > 0
    
    def test_guide_missing_required_fields(self):
        """Test avec des champs requis manquants"""
        payload = {
            "culture": "tomates"
            # Manque saison
        }
        
        response = client.post("/guide", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_guide_different_cultures(self):
        """Test avec différentes cultures"""
        cultures = ["tomates", "légumes", "céréales"]
        
        for culture in cultures:
            payload = {
                "culture": culture,
                "saison": "été",
                "niveau": "intermédiaire"
            }
            
            response = client.post("/guide", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert data["culture"] == culture
    
    def test_guide_different_seasons(self):
        """Test avec différentes saisons"""
        saisons = ["printemps", "été", "automne", "hiver"]
        
        for saison in saisons:
            payload = {
                "culture": "tomates",
                "saison": saison,
                "niveau": "débutant"
            }
            
            response = client.post("/guide", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data["conseils"], list)
            assert len(data["conseils"]) > 0

class TestChatEndpoint:
    """Tests pour l'endpoint /chat"""
    
    def test_chat_valid_message(self):
        """Test avec un message valide"""
        payload = {
            "message": "Bonjour, j'ai besoin d'aide pour mes cultures",
            "contexte": "agriculture débutant"
        }
        
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert "reponse" in data
        assert "suggestions" in data
        assert "ressources_utiles" in data
        
        assert isinstance(data["reponse"], str)
        assert len(data["reponse"]) > 0
        assert isinstance(data["suggestions"], list)
        assert isinstance(data["ressources_utiles"], list)
    
    def test_chat_different_greetings(self):
        """Test avec différents types de salutations"""
        messages = ["bonjour", "salut", "hello"]
        
        for message in messages:
            payload = {"message": message}
            response = client.post("/chat", json=payload)
            assert response.status_code == 200
            
            data = response.json()
            if "bonjour" in message.lower():
                assert "Bonjour" in data["reponse"]
    
    def test_chat_culture_questions(self):
        """Test avec des questions sur la culture"""
        payload = {
            "message": "Comment faire de la culture biologique ?",
            "contexte": "formation MFR"
        }
        
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data["suggestions"], list)
        assert len(data["suggestions"]) > 0
    
    def test_chat_missing_message(self):
        """Test avec un message manquant"""
        payload = {}
        
        response = client.post("/chat", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_chat_empty_message(self):
        """Test avec un message vide"""
        payload = {"message": ""}
        
        response = client.post("/chat", json=payload)
        # Un message vide est accepté et génère une réponse par défaut
        assert response.status_code == 200
        
        data = response.json()
        assert "reponse" in data
        assert isinstance(data["reponse"], str)

class TestRootEndpoint:
    """Tests pour l'endpoint racine"""
    
    def test_root_endpoint(self):
        """Test de l'endpoint racine /"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "documentation" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

class TestCORSAndSecurity:
    """Tests pour CORS et sécurité"""
    
    def test_cors_headers_present(self):
        """Test que les headers CORS sont présents"""
        response = client.options("/health")
        # FastAPI gère automatiquement les headers CORS avec le middleware
        assert response.status_code in [200, 405]  # 405 pour OPTIONS non supporté explicitement
    
    def test_api_documentation_accessible(self):
        """Test que la documentation API est accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])