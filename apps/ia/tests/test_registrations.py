"""
Tests pour les routes API des inscriptions
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date, timedelta
import sys
import os

# Ajouter le répertoire parent au PATH pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

class TestRegistrations:
    """Tests pour les endpoints des inscriptions"""
    
    def test_get_registrations_list(self):
        """Test de récupération de la liste des inscriptions"""
        response = client.get("/api/v1/registrations/")
        assert response.status_code == 200
        
        registrations = response.json()
        assert isinstance(registrations, list)
        
        # Vérifier la structure d'une inscription si elle existe
        if registrations:
            registration = registrations[0]
            required_fields = ["id", "activity_id", "participant_name", "participant_email", "status", "created_at"]
            for field in required_fields:
                assert field in registration
    
    def test_get_registrations_with_filters(self):
        """Test de filtrage des inscriptions"""
        # Filtrer par statut
        response = client.get("/api/v1/registrations/?status=pending")
        assert response.status_code == 200
        
        registrations = response.json()
        for registration in registrations:
            assert registration["status"] == "pending"
        
        # Filtrer par type de participant
        response = client.get("/api/v1/registrations/?participant_type=student_mfr")
        assert response.status_code == 200
        
        registrations = response.json()
        for registration in registrations:
            assert registration["participant_type"] == "student_mfr"
    
    def test_get_registration_by_id(self):
        """Test de récupération d'une inscription par ID"""
        # Utiliser un ID existant dans les données de test
        response = client.get("/api/v1/registrations/reg_001")
        assert response.status_code == 200
        
        registration = response.json()
        assert registration["id"] == "reg_001"
        assert "participant_name" in registration
        assert "activity_id" in registration
    
    def test_get_registration_by_id_not_found(self):
        """Test d'inscription non trouvée"""
        response = client.get("/api/v1/registrations/reg_999")
        assert response.status_code == 404
    
    def test_create_registration(self):
        """Test de création d'une nouvelle inscription"""
        tomorrow = date.today() + timedelta(days=1)
        
        new_registration = {
            "activity_id": "1",
            "participant_name": "Test User",
            "participant_email": "test@example.com",
            "participant_phone": "06 12 34 56 78",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1,
            "special_requirements": "Aucune"
        }
        
        response = client.post("/api/v1/registrations/", json=new_registration)
        assert response.status_code == 201
        
        created_registration = response.json()
        assert created_registration["participant_name"] == new_registration["participant_name"]
        assert created_registration["activity_id"] == new_registration["activity_id"]
        assert created_registration["status"] == "pending"
        assert "id" in created_registration
        assert "created_at" in created_registration
    
    def test_create_registration_past_date(self):
        """Test de création avec une date dans le passé"""
        yesterday = date.today() - timedelta(days=1)
        
        registration = {
            "activity_id": "1",
            "participant_name": "Test User",
            "participant_email": "test@example.com",
            "participant_type": "volunteer",
            "requested_date": yesterday.isoformat(),
            "participants_count": 1
        }
        
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 400
        assert "passé" in response.json()["detail"]
    
    def test_create_registration_invalid_activity(self):
        """Test de création avec une activité inexistante"""
        tomorrow = date.today() + timedelta(days=1)
        
        registration = {
            "activity_id": "999",  # Activité inexistante
            "participant_name": "Test User",
            "participant_email": "test@example.com",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1
        }
        
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 404
        assert "Activité non trouvée" in response.json()["detail"]
    
    def test_create_registration_validation_error(self):
        """Test de validation lors de la création"""
        invalid_registration = {
            "activity_id": "1",
            "participant_name": "",  # Nom vide
            "participant_email": "invalid-email",  # Email invalide
            "participant_type": "invalid_type",  # Type invalide
            "participants_count": 0  # Nombre invalide
        }
        
        response = client.post("/api/v1/registrations/", json=invalid_registration)
        assert response.status_code == 422  # Validation Error
    
    def test_update_registration(self):
        """Test de mise à jour d'une inscription"""
        update_data = {
            "status": "confirmed",
            "assigned_instructor": "Prof. Martin",
            "location": "Ferme de test"
        }
        
        response = client.put("/api/v1/registrations/reg_001", json=update_data)
        assert response.status_code == 200
        
        updated_registration = response.json()
        assert updated_registration["status"] == update_data["status"]
        assert updated_registration["assigned_instructor"] == update_data["assigned_instructor"]
        assert updated_registration["location"] == update_data["location"]
        assert "updated_at" in updated_registration
    
    def test_update_registration_not_found(self):
        """Test de mise à jour d'une inscription inexistante"""
        update_data = {"status": "confirmed"}
        
        response = client.put("/api/v1/registrations/reg_999", json=update_data)
        assert response.status_code == 404
    
    def test_cancel_registration(self):
        """Test d'annulation d'une inscription"""
        # D'abord créer une inscription à annuler
        tomorrow = date.today() + timedelta(days=1)
        
        new_registration = {
            "activity_id": "1",
            "participant_name": "To Cancel",
            "participant_email": "cancel@example.com",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1
        }
        
        create_response = client.post("/api/v1/registrations/", json=new_registration)
        created_registration = create_response.json()
        registration_id = created_registration["id"]
        
        # Annuler l'inscription
        response = client.delete(f"/api/v1/registrations/{registration_id}")
        assert response.status_code == 200
        
        # Vérifier que le statut est maintenant "cancelled"
        get_response = client.get(f"/api/v1/registrations/{registration_id}")
        assert get_response.status_code == 200
        cancelled_registration = get_response.json()
        assert cancelled_registration["status"] == "cancelled"
    
    def test_get_registrations_for_activity(self):
        """Test de récupération des inscriptions pour une activité"""
        response = client.get("/api/v1/registrations/activity/1")
        assert response.status_code == 200
        
        registrations = response.json()
        assert isinstance(registrations, list)
        
        # Toutes les inscriptions doivent être pour l'activité 1
        for registration in registrations:
            assert registration["activity_id"] == "1"
    
    def test_get_registrations_for_participant(self):
        """Test de récupération des inscriptions pour un participant"""
        email = "marie.dupont@example.com"
        response = client.get(f"/api/v1/registrations/participant/{email}")
        assert response.status_code == 200
        
        registrations = response.json()
        assert isinstance(registrations, list)
        
        # Toutes les inscriptions doivent être pour cet email
        for registration in registrations:
            assert registration["participant_email"] == email
    
    def test_get_registration_stats(self):
        """Test de récupération des statistiques"""
        response = client.get("/api/v1/registrations/stats/")
        assert response.status_code == 200
        
        stats = response.json()
        assert "total_registrations" in stats
        assert "pending_registrations" in stats
        assert "confirmed_registrations" in stats
        assert "registrations_by_activity" in stats
        assert "registrations_by_type" in stats
        
        # Vérifier que les chiffres sont cohérents
        total = stats["total_registrations"]
        pending = stats["pending_registrations"]
        confirmed = stats["confirmed_registrations"]
        completed = stats["completed_registrations"]
        cancelled = stats["cancelled_registrations"]
        
        assert pending + confirmed + completed + cancelled == total
    
    def test_confirm_registration(self):
        """Test de confirmation d'une inscription"""
        # D'abord créer une inscription à confirmer
        tomorrow = date.today() + timedelta(days=1)
        
        new_registration = {
            "activity_id": "1",
            "participant_name": "To Confirm",
            "participant_email": "confirm@example.com",
            "participant_type": "student_mfr",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1
        }
        
        create_response = client.post("/api/v1/registrations/", json=new_registration)
        created_registration = create_response.json()
        registration_id = created_registration["id"]
        
        # Confirmer l'inscription
        confirm_data = {
            "instructor": "Prof. Durand",
            "location": "Ferme principale"
        }
        
        response = client.post(f"/api/v1/registrations/{registration_id}/confirm", params=confirm_data)
        assert response.status_code == 200
        
        result = response.json()
        assert "message" in result
        assert "registration" in result
        
        confirmed_registration = result["registration"]
        assert confirmed_registration["status"] == "confirmed"
        assert confirmed_registration["assigned_instructor"] == confirm_data["instructor"]
        assert confirmed_registration["location"] == confirm_data["location"]
        assert confirmed_registration["confirmed_date"] is not None


class TestRegistrationValidation:
    """Tests de validation des données d'inscription"""
    
    def test_participant_name_validation(self):
        """Test de validation du nom du participant"""
        tomorrow = date.today() + timedelta(days=1)
        
        # Nom trop court
        registration = {
            "activity_id": "1",
            "participant_name": "A",
            "participant_email": "test@example.com",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1
        }
        
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 422
    
    def test_email_validation(self):
        """Test de validation de l'email"""
        tomorrow = date.today() + timedelta(days=1)
        
        registration = {
            "activity_id": "1",
            "participant_name": "Test User",
            "participant_email": "invalid-email",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": 1
        }
        
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 422
    
    def test_participants_count_validation(self):
        """Test de validation du nombre de participants"""
        tomorrow = date.today() + timedelta(days=1)
        
        # Nombre négatif
        registration = {
            "activity_id": "1",
            "participant_name": "Test User",
            "participant_email": "test@example.com",
            "participant_type": "volunteer",
            "requested_date": tomorrow.isoformat(),
            "participants_count": -1
        }
        
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 422
        
        # Nombre trop élevé
        registration["participants_count"] = 50
        response = client.post("/api/v1/registrations/", json=registration)
        assert response.status_code == 422


# Tests d'intégration
def test_full_registration_workflow():
    """Test du workflow complet d'inscription"""
    
    tomorrow = date.today() + timedelta(days=1)
    
    # 1. Créer une inscription
    new_registration = {
        "activity_id": "1",
        "participant_name": "Workflow Test User",
        "participant_email": "workflow@example.com",
        "participant_type": "volunteer",
        "requested_date": tomorrow.isoformat(),
        "participants_count": 2,
        "special_requirements": "Végétarien"
    }
    
    create_response = client.post("/api/v1/registrations/", json=new_registration)
    assert create_response.status_code == 201
    created = create_response.json()
    registration_id = created["id"]
    assert created["status"] == "pending"
    
    # 2. Confirmer l'inscription
    confirm_response = client.post(
        f"/api/v1/registrations/{registration_id}/confirm",
        params={"instructor": "Prof. Test", "location": "Ferme Test"}
    )
    assert confirm_response.status_code == 200
    
    # 3. Vérifier la confirmation
    get_response = client.get(f"/api/v1/registrations/{registration_id}")
    assert get_response.status_code == 200
    confirmed = get_response.json()
    assert confirmed["status"] == "confirmed"
    assert confirmed["assigned_instructor"] == "Prof. Test"
    assert confirmed["location"] == "Ferme Test"
    
    # 4. Mettre à jour des notes
    update_response = client.put(
        f"/api/v1/registrations/{registration_id}",
        json={"notes": "Participant très motivé"}
    )
    assert update_response.status_code == 200
    
    # 5. Marquer comme terminé
    complete_response = client.put(
        f"/api/v1/registrations/{registration_id}",
        json={"status": "completed"}
    )
    assert complete_response.status_code == 200
    
    # 6. Vérifier l'état final
    final_get_response = client.get(f"/api/v1/registrations/{registration_id}")
    final_registration = final_get_response.json()
    assert final_registration["status"] == "completed"
    assert final_registration["notes"] == "Participant très motivé"