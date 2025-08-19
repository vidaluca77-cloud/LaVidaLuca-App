"""
Activity API endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.activity import Activity as ActivityModel, ActivityCategory
from app.schemas.activity import Activity, ActivityCreate, ActivityUpdate, ActivitySuggestion
from app.schemas.user import UserProfile

router = APIRouter()


@router.post("/", response_model=Activity, status_code=status.HTTP_201_CREATED)
def create_activity(activity_in: ActivityCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle activité.
    """
    # Check if activity slug already exists
    existing_activity = db.query(ActivityModel).filter(ActivityModel.slug == activity_in.slug).first()
    if existing_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une activité avec ce slug existe déjà"
        )
    
    # Create new activity
    db_activity = ActivityModel(**activity_in.dict())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity


@router.get("/", response_model=List[Activity])
def get_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[ActivityCategory] = Query(None, description="Filtrer par catégorie"),
    difficulty_level: Optional[int] = Query(None, description="Filtrer par niveau de difficulté"),
    safety_level: Optional[int] = Query(None, description="Filtrer par niveau de sécurité"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des activités avec filtres optionnels.
    """
    query = db.query(ActivityModel).filter(ActivityModel.is_active == 1)
    
    if category:
        query = query.filter(ActivityModel.category == category)
    if difficulty_level:
        query = query.filter(ActivityModel.difficulty_level == difficulty_level)
    if safety_level:
        query = query.filter(ActivityModel.safety_level == safety_level)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=Activity)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une activité par son ID.
    """
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id, 
        ActivityModel.is_active == 1
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    return activity


@router.get("/slug/{activity_slug}", response_model=Activity)
def get_activity_by_slug(activity_slug: str, db: Session = Depends(get_db)):
    """
    Récupérer une activité par son slug.
    """
    activity = db.query(ActivityModel).filter(
        ActivityModel.slug == activity_slug, 
        ActivityModel.is_active == 1
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    return activity


@router.put("/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity_update: ActivityUpdate, db: Session = Depends(get_db)):
    """
    Mettre à jour une activité.
    """
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id, 
        ActivityModel.is_active == 1
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    
    # Update activity fields
    update_data = activity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une activité (soft delete).
    """
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id, 
        ActivityModel.is_active == 1
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    
    activity.is_active = 0
    db.commit()
    
    return None


@router.post("/suggestions", response_model=List[ActivitySuggestion])
def get_activity_suggestions(user_profile: UserProfile, db: Session = Depends(get_db)):
    """
    Obtenir des suggestions d'activités basées sur le profil utilisateur.
    Compatible avec l'algorithme de matching du frontend.
    """
    activities = db.query(ActivityModel).filter(ActivityModel.is_active == 1).all()
    suggestions = []
    
    for activity in activities:
        score = 0
        reasons = []
        
        # Compétences communes
        common_skills = [skill for skill in activity.skill_tags if skill in user_profile.skills]
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Préférences de catégories
        if activity.category.value in user_profile.preferences:
            score += 25
            reasons.append(f"Catégorie préférée : {activity.category.value}")
        
        # Bonus pour niveau de sécurité bas (plus accessible)
        if activity.safety_level == 1:
            score += 10
            reasons.append("Activité accessible (sécurité niveau 1)")
        
        # Bonus pour activités courtes (plus facilement planifiables)
        if activity.duration_min <= 90:
            score += 5
            reasons.append("Durée courte (facilement planifiable)")
        
        if score > 0:
            suggestions.append(ActivitySuggestion(
                activity=activity,
                score=score,
                reasons=reasons
            ))
    
    # Trier par score décroissant
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return suggestions[:10]  # Retourner top 10