from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.models.user import User
from app.models.activity import Activity
from app.schemas.user import UserProfile
from app.schemas.activity import ActivitySuggestion
from app.services.recommendations import RecommendationService

router = APIRouter()


@router.post("/", response_model=List[ActivitySuggestion])
async def get_recommendations(
    user_profile: UserProfile,
    max_recommendations: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered activity recommendations for a user profile"""
    # Get all active activities
    result = await db.execute(select(Activity).where(Activity.is_active == True))
    activities = result.scalars().all()
    
    if not activities:
        return []
    
    # Generate recommendations using AI service
    suggestions = await RecommendationService.generate_recommendations(
        user_profile=user_profile,
        activities=activities,
        max_recommendations=max_recommendations
    )
    
    return suggestions


@router.get("/me", response_model=List[ActivitySuggestion])
async def get_my_recommendations(
    max_recommendations: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered activity recommendations for the current user"""
    # Create user profile from current user data
    user_profile = UserProfile(
        skills=current_user.skills or [],
        availability=current_user.availability or [],
        location=current_user.location or "",
        preferences=current_user.preferences or []
    )
    
    # Get all active activities
    result = await db.execute(select(Activity).where(Activity.is_active == True))
    activities = result.scalars().all()
    
    if not activities:
        return []
    
    # Generate recommendations using AI service
    suggestions = await RecommendationService.generate_recommendations(
        user_profile=user_profile,
        activities=activities,
        max_recommendations=max_recommendations
    )
    
    return suggestions


@router.get("/popular", response_model=List[ActivitySuggestion])
async def get_popular_activities(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Get popular activities (fallback recommendations)"""
    # Get featured activities first, then others
    result = await db.execute(
        select(Activity)
        .where(Activity.is_active == True)
        .order_by(Activity.is_featured.desc(), Activity.created_at.desc())
        .limit(limit)
    )
    activities = result.scalars().all()
    
    # Convert to suggestion format with generic scores
    suggestions = []
    for i, activity in enumerate(activities):
        score = 0.9 - (i * 0.1)  # Decreasing score based on order
        suggestions.append(ActivitySuggestion(
            activity=activity,
            score=max(score, 0.1),
            reasons=["Activité populaire", "Recommandée par l'équipe"]
        ))
    
    return suggestions