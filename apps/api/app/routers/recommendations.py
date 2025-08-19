from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import User
from app.schemas.recommendation import RecommendationResponse, RecommendationRequest
from app.services.recommendation import RecommendationService
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/", response_model=RecommendationResponse)
def get_user_recommendations(
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations for the current user."""
    
    recommendation_service = RecommendationService(db)
    recommendations = recommendation_service.get_user_recommendations(current_user, limit)
    
    # Calculate profile completeness
    profile_fields = [
        current_user.bio,
        current_user.location,
        current_user.skills,
        current_user.preferences,
        current_user.availability
    ]
    
    completed_fields = len([field for field in profile_fields if field])
    profile_completeness = completed_fields / len(profile_fields)
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_activities=len(recommendations),
        user_profile_completeness=round(profile_completeness, 2)
    )


@router.post("/by-preferences", response_model=RecommendationResponse)
def get_recommendations_by_preferences(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get activity recommendations based on specified preferences (for anonymous users)."""
    
    recommendation_service = RecommendationService(db)
    recommendations = recommendation_service.get_activity_recommendations_by_preferences(
        skills=request.user_skills,
        preferences=request.user_preferences,
        availability=request.user_availability,
        limit=request.limit or 5
    )
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_activities=len(recommendations),
        user_profile_completeness=None  # Not applicable for anonymous requests
    )


@router.get("/categories")
def get_recommendation_categories():
    """Get available categories for activity filtering."""
    return {
        "categories": [
            {
                "id": "agri",
                "name": "Agriculture",
                "description": "Élevage, cultures, soins aux animaux",
                "skills": ["elevage", "hygiene", "soins_animaux", "sol", "plantes", "responsabilite"]
            },
            {
                "id": "transfo", 
                "name": "Transformation",
                "description": "Produits fermiers, cuisine, conservation",
                "skills": ["hygiene", "precision", "creativite", "rythme", "temps"]
            },
            {
                "id": "artisanat",
                "name": "Artisanat", 
                "description": "Construction, réparation, création",
                "skills": ["bois", "precision", "securite", "proprete", "finitions", "endurance", "esthetique"]
            },
            {
                "id": "nature",
                "name": "Environnement",
                "description": "Écologie, biodiversité, ressources",
                "skills": ["ecologie", "observation", "patience", "endurance", "respect_nature"]
            },
            {
                "id": "social",
                "name": "Animation",
                "description": "Accueil, pédagogie, événements", 
                "skills": ["accueil", "pedagogie", "expression", "equipe", "patience", "creativite", "contact"]
            }
        ]
    }


@router.get("/skills")
def get_available_skills():
    """Get list of available skills for user profiling."""
    return {
        "skills": [
            # Agriculture
            {"id": "elevage", "name": "Élevage", "category": "agri"},
            {"id": "hygiene", "name": "Hygiène", "category": "general"},
            {"id": "soins_animaux", "name": "Soins aux animaux", "category": "agri"},
            {"id": "sol", "name": "Travail du sol", "category": "agri"},
            {"id": "plantes", "name": "Culture des plantes", "category": "agri"},
            {"id": "responsabilite", "name": "Responsabilité", "category": "general"},
            
            # Transformation
            {"id": "precision", "name": "Précision", "category": "general"},
            {"id": "creativite", "name": "Créativité", "category": "general"},
            {"id": "rythme", "name": "Sens du rythme", "category": "transfo"},
            {"id": "temps", "name": "Gestion du temps", "category": "general"},
            
            # Artisanat
            {"id": "bois", "name": "Travail du bois", "category": "artisanat"},
            {"id": "securite", "name": "Sécurité", "category": "general"},
            {"id": "proprete", "name": "Propreté", "category": "general"},
            {"id": "finitions", "name": "Finitions", "category": "artisanat"},
            {"id": "endurance", "name": "Endurance", "category": "general"},
            {"id": "esthetique", "name": "Sens esthétique", "category": "artisanat"},
            
            # Nature
            {"id": "ecologie", "name": "Écologie", "category": "nature"},
            {"id": "observation", "name": "Observation", "category": "nature"},
            {"id": "patience", "name": "Patience", "category": "general"},
            {"id": "respect_nature", "name": "Respect de la nature", "category": "nature"},
            
            # Social
            {"id": "accueil", "name": "Accueil", "category": "social"},
            {"id": "pedagogie", "name": "Pédagogie", "category": "social"},
            {"id": "expression", "name": "Expression", "category": "social"},
            {"id": "equipe", "name": "Travail en équipe", "category": "general"},
            {"id": "contact", "name": "Contact humain", "category": "social"}
        ]
    }