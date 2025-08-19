"""
Tests pour les routes API des activités
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Ajouter le répertoire parent au PATH pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

class TestActivities:
    """Tests pour les endpoints des activités"""
    
    def test_get_activities_list(self):
        """Test de récupération de la liste des activités"""
        response = client.get("/api/v1/activities/")
        assert response.status_code == 200
        
        activities = response.json()
        assert isinstance(activities, list)
        assert len(activities) > 0
        
        # Vérifier la structure d'une activité
        activity = activities[0]
        required_fields = ["id", "title", "category", "summary", "duration_min", "skill_tags", "seasonality", "safety_level"]
        for field in required_fields:
            assert field in activity
    
    def test_get_activities_with_filters(self):
        """Test de filtrage des activités"""
        # Filtrer par catégorie
        response = client.get("/api/v1/activities/?category=agri")
        assert response.status_code == 200
        
        activities = response.json()
        for activity in activities:
            assert activity["category"] == "agri"
        
        # Filtrer par niveau de sécurité
        response = client.get("/api/v1/activities/?safety_level=1")
        assert response.status_code == 200
        
        activities = response.json()
        for activity in activities:
            assert activity["safety_level"] <= 1
    
    def test_get_activity_by_id(self):
        """Test de récupération d'une activité par ID"""
        response = client.get("/api/v1/activities/1")
        assert response.status_code == 200
        
        activity = response.json()
        assert activity["id"] == "1"
        assert "title" in activity
        assert "category" in activity
    
    def test_get_activity_by_id_not_found(self):
        """Test d'activité non trouvée"""
        response = client.get("/api/v1/activities/999")
        assert response.status_code == 404
    
    def test_get_activity_by_slug(self):
        """Test de récupération d'une activité par slug"""
        response = client.get("/api/v1/activities/slug/nourrir-soigner-moutons")
        assert response.status_code == 200
        
        activity = response.json()
        assert activity["slug"] == "nourrir-soigner-moutons"
    
    def test_get_activity_by_slug_not_found(self):
        """Test de slug non trouvé"""
        response = client.get("/api/v1/activities/slug/activite-inexistante")
        assert response.status_code == 404
    
    def test_create_activity(self):
        """Test de création d'une nouvelle activité"""
        new_activity = {
            "title": "Test Activity",
            "category": "agri",
            "summary": "Une activité de test",
            "duration_min": 60,
            "skill_tags": ["test", "automation"],
            "seasonality": ["toutes"],
            "safety_level": 1,
            "materials": ["gants"]
        }
        
        response = client.post("/api/v1/activities/", json=new_activity)
        assert response.status_code == 201
        
        created_activity = response.json()
        assert created_activity["title"] == new_activity["title"]
        assert created_activity["category"] == new_activity["category"]
        assert "id" in created_activity
        assert "slug" in created_activity
        assert "created_at" in created_activity
    
    def test_create_activity_validation_error(self):
        """Test de validation lors de la création"""
        invalid_activity = {
            "title": "",  # Titre vide
            "category": "invalid_category",  # Catégorie invalide
            "duration_min": -10,  # Durée négative
            "safety_level": 10  # Niveau de sécurité trop élevé
        }
        
        response = client.post("/api/v1/activities/", json=invalid_activity)
        assert response.status_code == 422  # Validation Error
    
    def test_update_activity(self):
        """Test de mise à jour d'une activité"""
        update_data = {
            "title": "Titre mis à jour",
            "duration_min": 120
        }
        
        response = client.put("/api/v1/activities/1", json=update_data)
        assert response.status_code == 200
        
        updated_activity = response.json()
        assert updated_activity["title"] == update_data["title"]
        assert updated_activity["duration_min"] == update_data["duration_min"]
        assert "updated_at" in updated_activity
    
    def test_update_activity_not_found(self):
        """Test de mise à jour d'une activité inexistante"""
        update_data = {"title": "Nouveau titre"}
        
        response = client.put("/api/v1/activities/999", json=update_data)
        assert response.status_code == 404
    
    def test_delete_activity(self):
        """Test de suppression d'une activité"""
        # D'abord créer une activité à supprimer
        new_activity = {
            "title": "Activité à supprimer",
            "category": "agri",
            "summary": "Sera supprimée",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1
        }
        
        create_response = client.post("/api/v1/activities/", json=new_activity)
        created_activity = create_response.json()
        activity_id = created_activity["id"]
        
        # Supprimer l'activité
        response = client.delete(f"/api/v1/activities/{activity_id}")
        assert response.status_code == 200
        
        # Vérifier qu'elle n'existe plus
        get_response = client.get(f"/api/v1/activities/{activity_id}")
        assert get_response.status_code == 404
    
    def test_suggest_activities(self):
        """Test de suggestion d'activités basée sur un profil"""
        user_profile = {
            "skills": ["elevage", "responsabilite"],
            "availability": ["weekend"],
            "location": "Provence",
            "preferences": ["agri"]
        }
        
        response = client.post("/api/v1/activities/suggest", json=user_profile)
        assert response.status_code == 200
        
        suggestions = response.json()
        assert isinstance(suggestions, list)
        
        # Vérifier la structure des suggestions
        if suggestions:
            suggestion = suggestions[0]
            assert "activity" in suggestion
            assert "score" in suggestion
            assert "reasons" in suggestion
            assert isinstance(suggestion["score"], int)
            assert isinstance(suggestion["reasons"], list)
    
    def test_get_categories(self):
        """Test de récupération des catégories"""
        response = client.get("/api/v1/activities/categories/")
        assert response.status_code == 200
        
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0
        
        # Vérifier la structure d'une catégorie
        category = categories[0]
        assert "id" in category
        assert "name" in category
        assert "description" in category
    
    def test_get_skills(self):
        """Test de récupération des compétences"""
        response = client.get("/api/v1/activities/skills/")
        assert response.status_code == 200
        
        skills = response.json()
        assert isinstance(skills, list)
        assert len(skills) > 0
        assert all(isinstance(skill, str) for skill in skills)


class TestActivityValidation:
    """Tests de validation des données d'activité"""
    
    def test_activity_title_validation(self):
        """Test de validation du titre"""
        # Titre trop court
        activity = {
            "title": "A",
            "category": "agri",
            "summary": "Test",
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1
        }
        
        response = client.post("/api/v1/activities/", json=activity)
        # Le titre très court devrait passer mais ce n'est pas optimal
        # En production, on ajouterait une validation min_length
    
    def test_activity_duration_validation(self):
        """Test de validation de la durée"""
        # Durée négative
        activity = {
            "title": "Test Activity",
            "category": "agri", 
            "summary": "Test",
            "duration_min": -10,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 1
        }
        
        response = client.post("/api/v1/activities/", json=activity)
        assert response.status_code == 422
    
    def test_activity_safety_level_validation(self):
        """Test de validation du niveau de sécurité"""
        # Niveau de sécurité trop élevé
        activity = {
            "title": "Test Activity",
            "category": "agri",
            "summary": "Test", 
            "duration_min": 60,
            "skill_tags": ["test"],
            "seasonality": ["toutes"],
            "safety_level": 10
        }
        
        response = client.post("/api/v1/activities/", json=activity)
        assert response.status_code == 422


@pytest.fixture(scope="module")
def test_client():
    """Fixture pour le client de test"""
    return client


# Tests d'intégration
def test_full_activity_workflow(test_client):
    """Test du workflow complet : création, lecture, mise à jour, suppression"""
    
    # 1. Créer une activité
    new_activity = {
        "title": "Workflow Test Activity",
        "category": "nature",
        "summary": "Test du workflow complet",
        "duration_min": 90,
        "skill_tags": ["patience", "observation"],
        "seasonality": ["printemps"],
        "safety_level": 1,
        "materials": ["jumelles"]
    }
    
    create_response = test_client.post("/api/v1/activities/", json=new_activity)
    assert create_response.status_code == 201
    created = create_response.json()
    activity_id = created["id"]
    
    # 2. Lire l'activité créée
    get_response = test_client.get(f"/api/v1/activities/{activity_id}")
    assert get_response.status_code == 200
    retrieved = get_response.json()
    assert retrieved["title"] == new_activity["title"]
    
    # 3. Mettre à jour l'activité
    update_data = {"summary": "Résumé mis à jour"}
    update_response = test_client.put(f"/api/v1/activities/{activity_id}", json=update_data)
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["summary"] == update_data["summary"]
    
    # 4. Supprimer l'activité
    delete_response = test_client.delete(f"/api/v1/activities/{activity_id}")
    assert delete_response.status_code == 200
    
    # 5. Vérifier que l'activité n'existe plus
    final_get_response = test_client.get(f"/api/v1/activities/{activity_id}")
    assert final_get_response.status_code == 404