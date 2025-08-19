"""
Activity and recommendation API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..core.deps import get_current_user
from ..models.models import Activity, User
from ..schemas.schemas import (
    Activity as ActivitySchema,
    RecommendationRequest,
    RecommendationResponse,
    UserProfileBase
)
from ..services.recommendation_service import RecommendationService

router = APIRouter()


@router.get("/activities", response_model=List[ActivitySchema])
async def get_activities(
    category: Optional[str] = Query(None, description="Filter by category"),
    skill_tag: Optional[str] = Query(None, description="Filter by skill tag"),
    safety_level: Optional[int] = Query(None, ge=1, le=3, description="Filter by safety level"),
    db: Session = Depends(get_db)
):
    """Get all activities with optional filters."""
    query = db.query(Activity)
    
    if category:
        query = query.filter(Activity.category == category)
    
    if skill_tag:
        query = query.filter(Activity.skill_tags.contains([skill_tag]))
    
    if safety_level:
        query = query.filter(Activity.safety_level == safety_level)
    
    activities = query.all()
    return activities


@router.get("/activities/{activity_id}", response_model=ActivitySchema)
async def get_activity(
    activity_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific activity by ID."""
    activity = db.query(Activity).filter(Activity.id == activity_id).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    return activity


@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get activity recommendations based on user profile."""
    recommendation_service = RecommendationService(db)
    
    # Get recommendations
    recommendations = await recommendation_service.get_recommendations(
        user_profile=request.user_profile,
        limit=request.limit
    )
    
    # Calculate profile completeness
    profile_completeness = _calculate_profile_completeness(request.user_profile)
    
    # Get total number of activities
    total_activities = db.query(Activity).count()
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_activities=total_activities,
        profile_completeness=profile_completeness
    )


@router.post("/recommendations/me", response_model=RecommendationResponse)
async def get_my_recommendations(
    limit: int = Query(5, ge=1, le=20, description="Number of recommendations"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get recommendations for the current authenticated user."""
    # Get user profile
    from ..models.models import UserProfile
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please create a profile first."
        )
    
    # Convert to UserProfileBase
    user_profile = UserProfileBase(
        skills=profile.skills or [],
        preferences=profile.preferences or [],
        availability=profile.availability or [],
        location=profile.location,
        experience_level=profile.experience_level,
        bio=profile.bio,
        phone=profile.phone
    )
    
    recommendation_service = RecommendationService(db)
    
    # Get recommendations
    recommendations = await recommendation_service.get_recommendations(
        user_profile=user_profile,
        limit=limit
    )
    
    # Calculate profile completeness
    profile_completeness = _calculate_profile_completeness(user_profile)
    
    # Get total number of activities
    total_activities = db.query(Activity).count()
    
    return RecommendationResponse(
        recommendations=recommendations,
        total_activities=total_activities,
        profile_completeness=profile_completeness
    )


def _calculate_profile_completeness(profile: UserProfileBase) -> float:
    """Calculate how complete a user profile is (0.0 to 1.0)."""
    total_fields = 6
    completed_fields = 0
    
    if profile.skills:
        completed_fields += 1
    if profile.preferences:
        completed_fields += 1
    if profile.availability:
        completed_fields += 1
    if profile.location:
        completed_fields += 1
    if profile.experience_level and profile.experience_level != "debutant":
        completed_fields += 1
    if profile.bio:
        completed_fields += 1
    
    return completed_fields / total_fields