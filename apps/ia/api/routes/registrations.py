"""
Routes API pour la gestion des inscriptions
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from enum import Enum
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Énumérations
class RegistrationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ParticipantType(str, Enum):
    STUDENT_MFR = "student_mfr"  # Élève MFR
    VOLUNTEER = "volunteer"      # Bénévole
    VISITOR = "visitor"         # Visiteur
    INSTRUCTOR = "instructor"   # Encadrant

# Modèles Pydantic
class RegistrationBase(BaseModel):
    activity_id: str = Field(..., description="ID de l'activité")
    participant_name: str = Field(..., description="Nom du participant", min_length=2, max_length=100)
    participant_email: EmailStr = Field(..., description="Email du participant")
    participant_phone: Optional[str] = Field(None, description="Téléphone du participant")
    participant_type: ParticipantType = Field(..., description="Type de participant")
    requested_date: date = Field(..., description="Date souhaitée pour l'activité")
    participants_count: int = Field(1, description="Nombre de participants", ge=1, le=20)
    special_requirements: Optional[str] = Field(None, description="Besoins spéciaux ou commentaires")
    emergency_contact: Optional[str] = Field(None, description="Contact d'urgence")

class Registration(RegistrationBase):
    id: str = Field(..., description="Identifiant unique de l'inscription")
    status: RegistrationStatus = Field(default=RegistrationStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    confirmed_date: Optional[datetime] = Field(None, description="Date de confirmation")
    assigned_instructor: Optional[str] = Field(None, description="Encadrant assigné")
    location: Optional[str] = Field(None, description="Lieu de l'activité")
    notes: Optional[str] = Field(None, description="Notes internes")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "reg_001",
                "activity_id": "1",
                "participant_name": "Marie Dupont",
                "participant_email": "marie.dupont@example.com",
                "participant_phone": "06 12 34 56 78",
                "participant_type": "student_mfr",
                "requested_date": "2024-04-15",
                "participants_count": 1,
                "status": "pending",
                "created_at": "2024-01-15T10:00:00Z"
            }
        }

class RegistrationCreate(RegistrationBase):
    pass

class RegistrationUpdate(BaseModel):
    status: Optional[RegistrationStatus] = None
    confirmed_date: Optional[datetime] = None
    assigned_instructor: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None
    special_requirements: Optional[str] = None

class RegistrationStats(BaseModel):
    total_registrations: int
    pending_registrations: int
    confirmed_registrations: int
    completed_registrations: int
    cancelled_registrations: int
    registrations_by_activity: dict
    registrations_by_type: dict

# Base de données simulée
REGISTRATIONS_DB = [
    {
        "id": "reg_001",
        "activity_id": "1",
        "participant_name": "Marie Dupont",
        "participant_email": "marie.dupont@example.com",
        "participant_phone": "06 12 34 56 78",
        "participant_type": "student_mfr",
        "requested_date": date(2024, 4, 15),
        "participants_count": 1,
        "status": "confirmed",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "confirmed_date": datetime.utcnow(),
        "assigned_instructor": "Jean Martin",
        "location": "Ferme pédagogique de Provence"
    },
    {
        "id": "reg_002",
        "activity_id": "2",
        "participant_name": "Pierre Bernard",
        "participant_email": "pierre.bernard@example.com",
        "participant_type": "volunteer",
        "requested_date": date(2024, 4, 20),
        "participants_count": 2,
        "status": "pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "special_requirements": "Préférence pour le matin"
    }
]

def generate_registration_id() -> str:
    """Génère un ID unique pour l'inscription"""
    import uuid
    return f"reg_{uuid.uuid4().hex[:8]}"

@router.get("/", response_model=List[Registration])
async def get_registrations(
    status: Optional[RegistrationStatus] = Query(None, description="Filtrer par statut"),
    activity_id: Optional[str] = Query(None, description="Filtrer par activité"),
    participant_type: Optional[ParticipantType] = Query(None, description="Filtrer par type de participant"),
    date_from: Optional[date] = Query(None, description="Date de début (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="Date de fin (YYYY-MM-DD)"),
    limit: int = Query(50, description="Nombre maximum d'inscriptions", le=200)
):
    """Récupère la liste des inscriptions avec filtres optionnels"""
    
    registrations = [Registration(**reg) for reg in REGISTRATIONS_DB]
    
    # Appliquer les filtres
    if status:
        registrations = [r for r in registrations if r.status == status]
    
    if activity_id:
        registrations = [r for r in registrations if r.activity_id == activity_id]
    
    if participant_type:
        registrations = [r for r in registrations if r.participant_type == participant_type]
    
    if date_from:
        registrations = [r for r in registrations if r.requested_date >= date_from]
    
    if date_to:
        registrations = [r for r in registrations if r.requested_date <= date_to]
    
    # Limiter les résultats
    registrations = registrations[:limit]
    
    logger.info(f"Retour de {len(registrations)} inscriptions")
    return registrations

@router.get("/{registration_id}", response_model=Registration)
async def get_registration(registration_id: str):
    """Récupère une inscription spécifique par son ID"""
    
    registration_data = next((r for r in REGISTRATIONS_DB if r["id"] == registration_id), None)
    if not registration_data:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    return Registration(**registration_data)

@router.post("/", response_model=Registration, status_code=201)
async def create_registration(registration: RegistrationCreate):
    """Crée une nouvelle inscription"""
    
    # Vérifier que l'activité existe (simulation)
    from .activities import ACTIVITIES_DB
    activity_exists = any(a["id"] == registration.activity_id for a in ACTIVITIES_DB)
    if not activity_exists:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    # Vérifier que la date n'est pas dans le passé
    if registration.requested_date < date.today():
        raise HTTPException(status_code=400, detail="La date demandée ne peut pas être dans le passé")
    
    # Générer un ID unique
    new_id = generate_registration_id()
    
    # Créer l'inscription
    now = datetime.utcnow()
    new_registration_data = {
        "id": new_id,
        "status": RegistrationStatus.PENDING,
        "created_at": now,
        "updated_at": now,
        "confirmed_date": None,
        "assigned_instructor": None,
        "location": None,
        "notes": None,
        **registration.dict()
    }
    
    REGISTRATIONS_DB.append(new_registration_data)
    
    logger.info(f"Nouvelle inscription créée: {new_registration_data['participant_name']} pour l'activité {registration.activity_id}")
    
    # En production, ici on enverrait un email de confirmation
    
    return Registration(**new_registration_data)

@router.put("/{registration_id}", response_model=Registration)
async def update_registration(registration_id: str, registration_update: RegistrationUpdate):
    """Met à jour une inscription existante"""
    
    registration_data = next((r for r in REGISTRATIONS_DB if r["id"] == registration_id), None)
    if not registration_data:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    # Mettre à jour les champs fournis
    update_data = registration_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            registration_data[field] = value
        registration_data["updated_at"] = datetime.utcnow()
        
        # Si on confirme l'inscription, mettre à jour la date de confirmation
        if update_data.get("status") == RegistrationStatus.CONFIRMED and not registration_data.get("confirmed_date"):
            registration_data["confirmed_date"] = datetime.utcnow()
    
    logger.info(f"Inscription mise à jour: {registration_id}")
    return Registration(**registration_data)

@router.delete("/{registration_id}")
async def cancel_registration(registration_id: str):
    """Annule une inscription (soft delete)"""
    
    registration_data = next((r for r in REGISTRATIONS_DB if r["id"] == registration_id), None)
    if not registration_data:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    # Marquer comme annulée au lieu de supprimer
    registration_data["status"] = RegistrationStatus.CANCELLED
    registration_data["updated_at"] = datetime.utcnow()
    
    logger.info(f"Inscription annulée: {registration_id}")
    
    return {"message": "Inscription annulée avec succès"}

@router.get("/activity/{activity_id}", response_model=List[Registration])
async def get_registrations_for_activity(
    activity_id: str,
    status: Optional[RegistrationStatus] = Query(None, description="Filtrer par statut")
):
    """Récupère toutes les inscriptions pour une activité spécifique"""
    
    registrations = [Registration(**reg) for reg in REGISTRATIONS_DB if reg["activity_id"] == activity_id]
    
    if status:
        registrations = [r for r in registrations if r.status == status]
    
    logger.info(f"Retour de {len(registrations)} inscriptions pour l'activité {activity_id}")
    return registrations

@router.get("/participant/{email}", response_model=List[Registration])
async def get_registrations_for_participant(email: EmailStr):
    """Récupère toutes les inscriptions pour un participant spécifique"""
    
    registrations = [Registration(**reg) for reg in REGISTRATIONS_DB if reg["participant_email"] == email]
    
    logger.info(f"Retour de {len(registrations)} inscriptions pour {email}")
    return registrations

@router.get("/stats/", response_model=RegistrationStats)
async def get_registration_stats():
    """Récupère les statistiques des inscriptions"""
    
    total = len(REGISTRATIONS_DB)
    
    # Compter par statut
    status_counts = {}
    for status in RegistrationStatus:
        status_counts[status.value] = sum(1 for r in REGISTRATIONS_DB if r["status"] == status.value)
    
    # Compter par activité
    activity_counts = {}
    for reg in REGISTRATIONS_DB:
        activity_id = reg["activity_id"]
        activity_counts[activity_id] = activity_counts.get(activity_id, 0) + 1
    
    # Compter par type de participant
    type_counts = {}
    for reg in REGISTRATIONS_DB:
        participant_type = reg["participant_type"]
        type_counts[participant_type] = type_counts.get(participant_type, 0) + 1
    
    stats = RegistrationStats(
        total_registrations=total,
        pending_registrations=status_counts.get("pending", 0),
        confirmed_registrations=status_counts.get("confirmed", 0),
        completed_registrations=status_counts.get("completed", 0),
        cancelled_registrations=status_counts.get("cancelled", 0),
        registrations_by_activity=activity_counts,
        registrations_by_type=type_counts
    )
    
    logger.info("Statistiques générées")
    return stats

@router.post("/{registration_id}/confirm")
async def confirm_registration(registration_id: str, instructor: Optional[str] = None, location: Optional[str] = None):
    """Confirme une inscription"""
    
    registration_data = next((r for r in REGISTRATIONS_DB if r["id"] == registration_id), None)
    if not registration_data:
        raise HTTPException(status_code=404, detail="Inscription non trouvée")
    
    if registration_data["status"] != RegistrationStatus.PENDING:
        raise HTTPException(status_code=400, detail="Seules les inscriptions en attente peuvent être confirmées")
    
    # Confirmer l'inscription
    registration_data["status"] = RegistrationStatus.CONFIRMED
    registration_data["confirmed_date"] = datetime.utcnow()
    registration_data["updated_at"] = datetime.utcnow()
    
    if instructor:
        registration_data["assigned_instructor"] = instructor
    if location:
        registration_data["location"] = location
    
    logger.info(f"Inscription confirmée: {registration_id}")
    
    # En production, ici on enverrait un email de confirmation
    
    return {"message": "Inscription confirmée avec succès", "registration": Registration(**registration_data)}