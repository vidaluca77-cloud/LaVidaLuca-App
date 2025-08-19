from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database import get_db
from models import Activity, Location, UserRole, ActivityCategory, SafetyLevel
from schemas import (
    ActivityCreate, ActivityUpdate, ActivityResponse, ActivitySummary,
    MessageResponse, PaginatedResponse, UserProfile, AIRecommendationRequest,
    AIRecommendationResponse, ActivitySuggestion
)
from routes.auth import get_current_active_user
from models import User

router = APIRouter()

def get_activity_by_id(db: Session, activity_id: int) -> Optional[Activity]:
    """Get activity by ID with location."""
    return db.query(Activity).options(joinedload(Activity.location)).filter(Activity.id == activity_id).first()

def get_activity_by_slug(db: Session, slug: str) -> Optional[Activity]:
    """Get activity by slug with location."""
    return db.query(Activity).options(joinedload(Activity.location)).filter(Activity.slug == slug).first()

def check_mentor_permission(current_user: User):
    """Check if user has mentor or admin permissions."""
    if current_user.role not in [UserRole.ADMIN, UserRole.MENTOR]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

@router.get("/", response_model=PaginatedResponse)
async def list_activities(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: Optional[ActivityCategory] = None,
    safety_level: Optional[SafetyLevel] = None,
    location_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List activities with filtering."""
    query = db.query(Activity).options(joinedload(Activity.location))
    
    # Apply filters
    if category:
        query = query.filter(Activity.category == category)
    if safety_level:
        query = query.filter(Activity.safety_level == safety_level)
    if location_id:
        query = query.filter(Activity.location_id == location_id)
    if is_active is not None:
        query = query.filter(Activity.is_active == is_active)
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Activity.title.ilike(search_term) |
            Activity.summary.ilike(search_term) |
            Activity.description.ilike(search_term)
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * size
    activities = query.offset(offset).limit(size).all()
    
    return PaginatedResponse(
        items=[ActivityResponse.from_orm(activity) for activity in activities],
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )

@router.get("/categories", response_model=List[str])
async def get_activity_categories():
    """Get all activity categories."""
    return [category.value for category in ActivityCategory]

@router.get("/summary", response_model=List[ActivitySummary])
async def get_activities_summary(
    category: Optional[ActivityCategory] = None,
    db: Session = Depends(get_db)
):
    """Get activities summary for quick display."""
    query = db.query(Activity).options(joinedload(Activity.location))
    
    if category:
        query = query.filter(Activity.category == category)
    
    query = query.filter(Activity.is_active == True)
    activities = query.all()
    
    return [
        ActivitySummary(
            id=activity.id,
            slug=activity.slug,
            title=activity.title,
            category=activity.category,
            summary=activity.summary,
            duration_min=activity.duration_min,
            safety_level=activity.safety_level,
            location_name=activity.location.name if activity.location else None
        )
        for activity in activities
    ]

@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_data: ActivityCreate,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Create new activity (mentor/admin only)."""
    check_mentor_permission(current_user)
    
    # Check if slug already exists
    if get_activity_by_slug(db, activity_data.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Activity with this slug already exists"
        )
    
    # Check if location exists
    if activity_data.location_id:
        location = db.query(Location).filter(Location.id == activity_data.location_id).first()
        if not location:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location not found"
            )
    
    # Create activity
    activity_dict = activity_data.dict(exclude={"skill_tags", "materials"})
    db_activity = Activity(**activity_dict)
    
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    # TODO: Add skill_tags and materials to association tables
    
    return db_activity

@router.get("/{activity_id}", response_model=ActivityResponse)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get activity by ID."""
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.get("/slug/{slug}", response_model=ActivityResponse)
async def get_activity_by_slug_endpoint(
    slug: str,
    db: Session = Depends(get_db)
):
    """Get activity by slug."""
    activity = get_activity_by_slug(db, slug)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity

@router.put("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: int,
    activity_update: ActivityUpdate,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Update activity (mentor/admin only)."""
    check_mentor_permission(current_user)
    
    activity = get_activity_by_id(db, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Update activity fields
    update_data = activity_update.dict(exclude_unset=True, exclude={"skill_tags", "materials"})
    for field, value in update_data.items():
        setattr(activity, field, value)
    
    db.commit()
    db.refresh(activity)
    
    # TODO: Update skill_tags and materials in association tables
    
    return activity

@router.delete("/{activity_id}", response_model=MessageResponse)
async def delete_activity(
    activity_id: int,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Deactivate activity (admin only)."""
    if current_user.role != UserRole.ADMIN:
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
    
    return MessageResponse(message="Activity deactivated successfully")

@router.post("/recommend", response_model=AIRecommendationResponse)
async def recommend_activities(
    request: AIRecommendationRequest,
    db: Session = Depends(lambda: None),  # Will be injected properly
    current_user: User = Depends(get_current_active_user)
):
    """Get AI-powered activity recommendations."""
    # Get all active activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    suggestions = []
    profile = request.user_profile
    
    for activity in activities:
        score = 0
        reasons = []
        
        # Category preference matching
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
        
        # Duration adaptation
        if activity.duration_min <= 90:
            score += 10
            reasons.append('Durée adaptée pour débuter')
        
        # Safety level
        if activity.safety_level.value <= 2:
            score += 10
            if activity.safety_level.value == 1:
                reasons.append('Activité sans risque particulier')
        
        # Location matching
        if profile.location and activity.location and profile.location.lower() in activity.location.name.lower():
            score += 20
            reasons.append('Proche de votre localisation')
        
        # Availability (simulation)
        if 'weekend' in profile.availability or 'semaine' in profile.availability:
            score += 15
            reasons.append('Compatible avec vos disponibilités')
        
        if score > 0:
            suggestions.append(ActivitySuggestion(
                activity=ActivityResponse.from_orm(activity),
                score=score,
                reasons=reasons
            ))
    
    # Sort by score and limit results
    suggestions.sort(key=lambda x: x.score, reverse=True)
    suggestions = suggestions[:request.limit]
    
    return AIRecommendationResponse(
        suggestions=suggestions,
        reasoning=f"Basé sur vos préférences ({', '.join(profile.preferences)}) et votre profil"
    )