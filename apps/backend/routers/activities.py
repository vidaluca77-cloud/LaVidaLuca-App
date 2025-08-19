from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import get_db
from models import Activity, Skill, User, ActivitySuggestion
from schemas import (
    Activity as ActivitySchema, ActivityCreate, ActivityUpdate,
    ActivitiesResponse, Suggestion, SuggestionsResponse, MatchingRequest,
    SafetyGuide, UserProfile
)
from routers.auth import get_current_active_user

router = APIRouter()

def get_activity_by_id(db: Session, activity_id: int) -> Optional[Activity]:
    """Get activity by ID"""
    return db.query(Activity).filter(Activity.id == activity_id).first()

def get_activity_by_slug(db: Session, slug: str) -> Optional[Activity]:
    """Get activity by slug"""
    return db.query(Activity).filter(Activity.slug == slug).first()

def calculate_matching_score(user_profile: UserProfile, activity: Activity) -> tuple[float, List[str]]:
    """Calculate matching score between user profile and activity"""
    score = 0.0
    reasons = []
    
    # Parse activity skill tags from JSON if stored as string
    activity_skills = []
    if hasattr(activity, 'skill_tags') and activity.skill_tags:
        if isinstance(activity.skill_tags, str):
            try:
                activity_skills = json.loads(activity.skill_tags)
            except json.JSONDecodeError:
                activity_skills = activity.skill_tags.split(',')
        else:
            activity_skills = activity.skill_tags
    
    # Common skills matching
    common_skills = [skill for skill in activity_skills if skill in user_profile.skills]
    if common_skills:
        score += len(common_skills) * 15
        reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
    
    # Category preferences
    if activity.category in user_profile.preferences:
        score += 25
        reasons.append(f"Catégorie préférée : {activity.category}")
    
    # Location bonus (simplified - could be enhanced with actual location matching)
    if user_profile.location:
        score += 5
        reasons.append("Profil localisé")
    
    # Availability bonus (simplified)
    if user_profile.availability:
        score += 10
        reasons.append("Disponibilité renseignée")
    
    # Safety level consideration (beginners get lower safety level activities)
    skill_count = len(user_profile.skills)
    if skill_count <= 3 and activity.safety_level == 1:
        score += 10
        reasons.append("Activité adaptée aux débutants")
    elif skill_count > 5 and activity.safety_level > 1:
        score += 5
        reasons.append("Activité pour profil expérimenté")
    
    return score, reasons

@router.get("/", response_model=ActivitiesResponse)
async def get_activities(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get list of activities with pagination and filters"""
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Apply filters
    if category:
        query = query.filter(Activity.category == category)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            Activity.title.ilike(search_filter) |
            Activity.summary.ilike(search_filter) |
            Activity.description.ilike(search_filter)
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    activities = query.offset((page - 1) * per_page).limit(per_page).all()
    
    return ActivitiesResponse(
        activities=activities,
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/{activity_id}", response_model=ActivitySchema)
async def get_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get activity by ID"""
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    return activity

@router.get("/slug/{slug}", response_model=ActivitySchema)
async def get_activity_by_slug_endpoint(slug: str, db: Session = Depends(get_db)):
    """Get activity by slug"""
    activity = get_activity_by_slug(db, slug)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    return activity

@router.post("/", response_model=ActivitySchema)
async def create_activity(
    activity_data: ActivityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new activity (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if activity with slug already exists
    if get_activity_by_slug(db, activity_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    # Create activity
    db_activity = Activity(
        slug=activity_data.slug,
        title=activity_data.title,
        category=activity_data.category.value,
        summary=activity_data.summary,
        description=activity_data.description,
        duration_min=activity_data.duration_min,
        safety_level=activity_data.safety_level,
        seasonality=json.dumps(activity_data.seasonality) if activity_data.seasonality else None,
        materials=json.dumps(activity_data.materials) if activity_data.materials else None
    )
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return db_activity

@router.put("/{activity_id}", response_model=ActivitySchema)
async def update_activity(
    activity_id: int,
    activity_data: ActivityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update activity (admin only)"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Update fields
    update_data = activity_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field in ["seasonality", "materials", "skill_tags"] and value is not None:
            value = json.dumps(value)
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    return activity

@router.delete("/{activity_id}")
async def delete_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete activity (admin only) - soft delete"""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    activity.is_active = False
    db.commit()
    
    return {"message": "Activity deleted successfully"}

@router.post("/match", response_model=SuggestionsResponse)
async def get_activity_suggestions(
    matching_request: MatchingRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get activity suggestions based on user profile"""
    user_profile = matching_request.user_profile
    
    # Get all active activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    # Calculate suggestions
    suggestions = []
    for activity in activities:
        score, reasons = calculate_matching_score(user_profile, activity)
        if score > 0:  # Only include activities with positive scores
            suggestions.append(Suggestion(
                activity=activity,
                score=score,
                reasons=reasons
            ))
    
    # Sort by score (descending)
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    # Limit to top 10 suggestions
    suggestions = suggestions[:10]
    
    # Store suggestions if user is authenticated
    if current_user:
        for suggestion in suggestions:
            db_suggestion = ActivitySuggestion(
                user_id=current_user.id,
                activity_id=suggestion.activity.id,
                score=suggestion.score,
                reasons=json.dumps(suggestion.reasons)
            )
            db.add(db_suggestion)
        db.commit()
    
    return SuggestionsResponse(
        suggestions=suggestions,
        user_profile=user_profile
    )

@router.get("/{activity_id}/safety-guide", response_model=SafetyGuide)
async def get_safety_guide(activity_id: int, db: Session = Depends(get_db)):
    """Get safety guide for an activity"""
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Generate safety rules based on activity properties
    rules = [
        "Respecter les consignes de l'encadrant",
        "Vérifier la présence de l'encadrant",
        "S'assurer d'avoir tous les matériels nécessaires",
        "Prendre connaissance des consignes de sécurité"
    ]
    
    checklist = [
        "Vérifier la présence de l'encadrant",
        "S'assurer d'avoir tous les matériels nécessaires",
        "Prendre connaissance des consignes de sécurité"
    ]
    
    # Add safety level specific rules
    if activity.safety_level >= 2:
        rules.extend([
            "Ne jamais agir seul, toujours en binôme minimum",
            "Vérifier deux fois avant d'utiliser un outil"
        ])
        checklist.extend([
            "Vérifier l'état des outils avant utilisation",
            "S'assurer de la présence d'une trousse de premiers secours"
        ])
    
    # Parse materials from JSON
    materials = []
    if activity.materials:
        try:
            materials = json.loads(activity.materials)
        except json.JSONDecodeError:
            materials = activity.materials.split(',') if activity.materials else []
    
    return SafetyGuide(
        activity_id=activity.id,
        rules=rules,
        checklist=checklist,
        materials=materials
    )