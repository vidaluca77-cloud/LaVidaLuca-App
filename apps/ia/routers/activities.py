from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Activity
from schemas import Activity as ActivitySchema, ActivityCreate, ActivityUpdate
from auth import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[ActivitySchema])
def get_activities(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Obtenir la liste des activités avec filtres optionnels"""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            Activity.title.ilike(search_term) | 
            Activity.summary.ilike(search_term) |
            Activity.description.ilike(search_term)
        )
    
    activities = query.offset(skip).limit(limit).all()
    return activities

@router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    """Obtenir la liste des catégories d'activités"""
    categories = db.query(Activity.category).filter(Activity.is_active == True).distinct().all()
    return [cat[0] for cat in categories]

@router.get("/skills")
def get_skills(db: Session = Depends(get_db)):
    """Obtenir la liste de toutes les compétences utilisées dans les activités"""
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    skills = set()
    for activity in activities:
        if activity.skill_tags:
            skills.update(activity.skill_tags)
    return sorted(list(skills))

@router.get("/{activity_id}", response_model=ActivitySchema)
def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Obtenir une activité par son ID"""
    activity = db.query(Activity).filter(
        Activity.id == activity_id,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.get("/slug/{slug}", response_model=ActivitySchema)
def get_activity_by_slug(slug: str, db: Session = Depends(get_db)):
    """Obtenir une activité par son slug"""
    activity = db.query(Activity).filter(
        Activity.slug == slug,
        Activity.is_active == True
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity