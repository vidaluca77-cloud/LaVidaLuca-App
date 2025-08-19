from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.activity import Activity as ActivityModel, ActivityCategory
from app.schemas.activity import Activity, ActivityCreate, ActivityUpdate, ActivitySummary, ActivityMatch
from app.schemas.user import UserProfile

router = APIRouter()


@router.get("/", response_model=List[ActivitySummary])
def read_activities(
    skip: int = 0,
    limit: int = 100,
    category: ActivityCategory = None,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des activités"""
    query = db.query(ActivityModel).filter(ActivityModel.is_active == True)
    
    if category:
        query = query.filter(ActivityModel.category == category)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.post("/", response_model=Activity)
def create_activity(activity: ActivityCreate, db: Session = Depends(get_db)):
    """Créer une nouvelle activité"""
    # Vérifier si le slug existe déjà
    db_activity = db.query(ActivityModel).filter(ActivityModel.slug == activity.slug).first()
    if db_activity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Une activité avec ce slug existe déjà"
        )
    
    # Créer l'activité
    db_activity = ActivityModel(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity


@router.get("/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    """Récupérer une activité par ID"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    return activity


@router.get("/slug/{slug}", response_model=Activity)
def read_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Récupérer une activité par slug"""
    activity = db.query(ActivityModel).filter(
        ActivityModel.slug == slug,
        ActivityModel.is_active == True
    ).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    return activity


@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une activité"""
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activité non trouvée"
        )
    
    # Mettre à jour les champs fournis
    update_data = activity_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    return activity


@router.post("/match", response_model=List[ActivityMatch])
def match_activities(profile: UserProfile, db: Session = Depends(get_db)):
    """Algorithme de matching d'activités basé sur le profil utilisateur"""
    activities = db.query(ActivityModel).filter(ActivityModel.is_active == True).all()
    suggestions = []
    
    for activity in activities:
        score = 0
        reasons = []
        
        # Compétences communes
        common_skills = [skill for skill in activity.skill_tags if skill in profile.skills]
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Préférences de catégories
        if activity.category.value in profile.preferences:
            score += 25
            category_names = {
                'agri': 'Agriculture',
                'transfo': 'Transformation',
                'artisanat': 'Artisanat',
                'nature': 'Environnement',
                'social': 'Animation'
            }
            reasons.append(f"Catégorie préférée : {category_names.get(activity.category.value, activity.category.value)}")
        
        # Durée adaptée
        if activity.duration_min <= 90:
            score += 10
            reasons.append('Durée adaptée pour débuter')
        
        # Sécurité
        if activity.safety_level <= 2:
            score += 10
            if activity.safety_level == 1:
                reasons.append('Activité sans risque particulier')
        
        # Disponibilité (simulation)
        if 'weekend' in profile.availability or 'semaine' in profile.availability:
            score += 15
            reasons.append('Compatible avec vos disponibilités')
        
        if score > 0:
            suggestions.append(ActivityMatch(
                activity=activity,
                score=score,
                reasons=reasons
            ))
    
    # Trier par score décroissant et limiter à 10 résultats
    suggestions.sort(key=lambda x: x.score, reverse=True)
    return suggestions[:10]


@router.get("/categories/", response_model=List[str])
def get_categories():
    """Récupérer la liste des catégories d'activités"""
    return [category.value for category in ActivityCategory]