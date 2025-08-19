"""
AI-powered activity suggestions routes using OpenAI integration.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import openai

from ..database import get_db_session
from ..models.user import User
from ..models.activity import Activity
from ..schemas.common import ApiResponse
from ..auth.dependencies import get_current_active_user
from ..config import settings
from ..services.openai_service import get_activity_suggestions, SuggestionRequest


router = APIRouter()


@router.post("/", response_model=ApiResponse[List[dict]])
async def get_personalized_suggestions(
    request: SuggestionRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get personalized activity suggestions using AI based on user profile.
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI suggestions service is not available"
        )
    
    try:
        # Get user's profile for enhanced personalization
        from ..models.profile import Profile
        profile_result = await db.execute(select(Profile).where(Profile.user_id == current_user.id))
        user_profile_obj = profile_result.scalar_one_or_none()
        
        if user_profile_obj:
            # Use detailed profile information
            user_profile = user_profile_obj.to_dict()
        else:
            # Fallback to basic user profile if no detailed profile exists
            user_profile = current_user.profile or {}
        
        # Get available activities from database
        activities_result = await db.execute(
            select(Activity).where(Activity.is_published == True)
        )
        activities = activities_result.scalars().all()
        
        # Generate suggestions using OpenAI with enhanced profile
        suggestions = await get_activity_suggestions(
            user_profile=user_profile,
            user_request=request.request,
            available_activities=[activity.to_dict() for activity in activities],
            max_suggestions=request.max_suggestions
        )
        
        return ApiResponse(
            success=True,
            data=suggestions,
            message="Personalized suggestions generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )


@router.get("/featured", response_model=ApiResponse[List[dict]])
async def get_featured_suggestions(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get featured activities as suggestions (no authentication required).
    """
    activities_result = await db.execute(
        select(Activity)
        .where(Activity.is_published == True, Activity.is_featured == True)
        .limit(limit)
        .order_by(Activity.created_at.desc())
    )
    activities = activities_result.scalars().all()
    
    suggestions = []
    for activity in activities:
        suggestions.append({
            "activity": activity.to_dict(),
            "score": 1.0,  # Featured activities get max score
            "reasons": [
                "Activité mise en avant",
                "Recommandée par l'équipe La Vida Luca"
            ]
        })
    
    return ApiResponse(
        success=True,
        data=suggestions,
        message="Featured suggestions retrieved successfully"
    )


@router.get("/similar/{activity_id}", response_model=ApiResponse[List[dict]])
async def get_similar_activities(
    activity_id: str,
    limit: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get activities similar to a specific activity.
    """
    # Get the reference activity
    result = await db.execute(
        select(Activity).where(Activity.id == activity_id, Activity.is_published == True)
    )
    reference_activity = result.scalar_one_or_none()
    
    if not reference_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Find similar activities based on category and tags
    similar_result = await db.execute(
        select(Activity)
        .where(
            Activity.is_published == True,
            Activity.id != activity_id,
            Activity.category == reference_activity.category
        )
        .limit(limit)
        .order_by(Activity.created_at.desc())
    )
    similar_activities = similar_result.scalars().all()
    
    suggestions = []
    for activity in similar_activities:
        # Calculate similarity score based on shared tags
        shared_tags = set(activity.skill_tags or []) & set(reference_activity.skill_tags or [])
        score = min(0.5 + (len(shared_tags) * 0.1), 1.0)
        
        reasons = [f"Même catégorie: {activity.category}"]
        if shared_tags:
            reasons.append(f"Compétences similaires: {', '.join(list(shared_tags)[:3])}")
        
        suggestions.append({
            "activity": activity.to_dict(),
            "score": score,
            "reasons": reasons
        })
    
    # Sort by score descending
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    
    return ApiResponse(
        success=True,
        data=suggestions,
        message="Similar activities retrieved successfully"
    )