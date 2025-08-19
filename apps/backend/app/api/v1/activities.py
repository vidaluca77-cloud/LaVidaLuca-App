from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.activity import Activity

router = APIRouter()


class ActivityResponse(BaseModel):
    id: int
    slug: str
    title: str
    category: str
    summary: str
    description: str = None
    duration_min: int
    skill_tags: list = []
    seasonality: list = []
    safety_level: int = 1
    materials: list = []
    location: str = None
    max_participants: int = 10
    min_age: int = 14
    is_mfr_only: bool = False
    pedagogical_objectives: list = []
    difficulty_level: int = 1
    is_active: bool = True

    class Config:
        from_attributes = True


class ActivityCreate(BaseModel):
    slug: str
    title: str
    category: str
    summary: str
    description: str = None
    duration_min: int
    skill_tags: List[str] = []
    seasonality: List[str] = []
    safety_level: int = 1
    materials: List[str] = []
    location: str = None
    max_participants: int = 10
    min_age: int = 14
    is_mfr_only: bool = False
    pedagogical_objectives: List[str] = []
    difficulty_level: int = 1


@router.get("/", response_model=List[ActivityResponse])
def get_activities(
    db: Session = Depends(get_db),
    category: Optional[str] = Query(None, description="Filtrer par catégorie"),
    skill: Optional[str] = Query(None, description="Filtrer par compétence requise"),
    max_duration: Optional[int] = Query(None, description="Durée maximale en minutes"),
    safety_level: Optional[int] = Query(None, description="Niveau de sécurité maximum"),
    mfr_only: Optional[bool] = Query(None, description="Activités réservées MFR uniquement"),
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=100, description="Nombre maximum d'éléments à retourner")
) -> Any:
    """
    Récupérer la liste des activités avec filtres optionnels
    """
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if skill:
        query = query.filter(Activity.skill_tags.contains([skill]))
    
    if max_duration:
        query = query.filter(Activity.duration_min <= max_duration)
    
    if safety_level:
        query = query.filter(Activity.safety_level <= safety_level)
    
    if mfr_only is not None:
        query = query.filter(Activity.is_mfr_only == mfr_only)
    
    activities = query.offset(skip).limit(limit).all()
    return activities


@router.get("/{activity_id}", response_model=ActivityResponse)
def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupérer une activité par son ID
    """
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    return activity


@router.get("/slug/{slug}", response_model=ActivityResponse)
def get_activity_by_slug(
    slug: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupérer une activité par son slug
    """
    activity = db.query(Activity).filter(
        Activity.slug == slug,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=404,
            detail="Activité non trouvée"
        )
    
    return activity


@router.get("/categories/", response_model=List[str])
def get_activity_categories(db: Session = Depends(get_db)) -> Any:
    """
    Récupérer la liste des catégories d'activités disponibles
    """
    categories = db.query(Activity.category).filter(
        Activity.is_active == True
    ).distinct().all()
    
    return [cat[0] for cat in categories]


@router.get("/skills/", response_model=List[str])
def get_activity_skills(db: Session = Depends(get_db)) -> Any:
    """
    Récupérer la liste de toutes les compétences requises
    """
    # Cette méthode nécessiterait une requête plus complexe pour extraire
    # tous les skills des champs JSON. Pour le moment, retourner une liste statique.
    skills = [
        'elevage', 'hygiene', 'soins_animaux', 'sol', 'plantes', 'organisation',
        'securite', 'bois', 'precision', 'creativite', 'patience', 'endurance',
        'ecologie', 'accueil', 'pedagogie', 'expression', 'equipe', 'responsabilite',
        'rythme', 'geste_utile', 'respect', 'rigueur', 'relationnel', 'contact',
        'compter_simple', 'temps'
    ]
    return skills


@router.post("/match", response_model=List[ActivityResponse])
def match_activities_to_user(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Any:
    """
    Trouver les activités correspondant au profil de l'utilisateur
    """
    # Récupérer toutes les activités actives
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    # Logique de matching simplifiée basée sur les compétences et préférences
    matched_activities = []
    
    for activity in activities:
        # Vérifier les préférences de catégorie
        if current_user.preferences and activity.category in current_user.preferences:
            matched_activities.append(activity)
            continue
        
        # Vérifier les compétences communes
        if current_user.skills and activity.skill_tags:
            common_skills = set(current_user.skills) & set(activity.skill_tags)
            if common_skills:
                matched_activities.append(activity)
    
    # Limiter à 10 résultats
    return matched_activities[:10]