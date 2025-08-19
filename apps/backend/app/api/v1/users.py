from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.services.auth import AuthService

router = APIRouter()


class UserProfileUpdate(BaseModel):
    skills: List[str] = []
    availability: List[str] = []
    location: str = None
    preferences: List[str] = []
    is_mfr_student: bool = False
    mfr_institution: str = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str = None
    is_active: bool
    skills: list = []
    availability: list = []
    location: str = None
    preferences: list = []
    is_mfr_student: bool = False
    mfr_institution: str = None

    class Config:
        from_attributes = True


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Récupérer le profil complet de l'utilisateur actuel
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Mettre à jour le profil de l'utilisateur actuel
    """
    auth_service = AuthService(db)
    
    profile_data = profile_update.dict(exclude_unset=True)
    updated_user = auth_service.update_user_profile(
        user_id=current_user.id,
        profile_data=profile_data
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    
    return updated_user


@router.get("/me/recommendations")
def get_user_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Obtenir des recommandations d'activités pour l'utilisateur
    """
    # TODO: Implémenter la logique de recommandation basée sur le profil
    # Pour l'instant, retourner un placeholder
    return {
        "message": "Recommandations à implémenter",
        "user_skills": current_user.skills,
        "user_preferences": current_user.preferences
    }