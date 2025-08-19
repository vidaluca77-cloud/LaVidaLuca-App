from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import Activity, User, Recommendation
from app.schemas.schemas import RecommendationRequest, RecommendationResponse, UserBase
from app.services.openai_service import openai_service
from app.utils.dependencies import get_current_active_user

router = APIRouter()


@router.post("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get AI-powered activity recommendations for a user."""
    
    # Use provided user profile or current user's profile
    if request.user_profile:
        user_profile = request.user_profile
    else:
        user_profile = UserBase(
            email=current_user.email,
            username=current_user.username,
            full_name=current_user.full_name,
            location=current_user.location,
            skills=current_user.skills or [],
            availability=current_user.availability or [],
            preferences=current_user.preferences or []
        )
    
    # Get all active activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities available"
        )
    
    # Convert to response format for the AI service
    activity_responses = [
        {
            "id": activity.id,
            "slug": activity.slug,
            "title": activity.title,
            "category": activity.category,
            "summary": activity.summary,
            "description": activity.description,
            "duration_min": activity.duration_min,
            "skill_tags": activity.skill_tags or [],
            "seasonality": activity.seasonality or [],
            "safety_level": activity.safety_level,
            "materials": activity.materials or [],
            "is_active": activity.is_active,
            "created_at": activity.created_at,
            "updated_at": activity.updated_at
        }
        for activity in activities
    ]
    
    # Get AI recommendations
    ai_recommendations = await openai_service.generate_recommendations(
        user_profile, activity_responses
    )
    
    # Store recommendations in database for analytics
    for rec in ai_recommendations[:request.limit]:
        db_recommendation = Recommendation(
            user_id=current_user.id,
            activity_id=rec["activity"]["id"],
            score=rec["score"],
            reasons=rec["reasons"]
        )
        db.add(db_recommendation)
    
    db.commit()
    
    # Convert to response format
    response_recommendations = []
    for rec in ai_recommendations[:request.limit]:
        activity_data = rec["activity"]
        
        # Find the actual activity object for proper response formatting
        activity_obj = next(
            (a for a in activities if a.id == activity_data["id"]), 
            None
        )
        
        if activity_obj:
            response_recommendations.append(
                RecommendationResponse(
                    id=0,  # This would be set if we returned the stored recommendation
                    activity=activity_obj,
                    score=rec["score"],
                    reasons=rec["reasons"],
                    created_at=activity_obj.created_at  # Using activity created_at as placeholder
                )
            )
    
    return response_recommendations


@router.get("/history", response_model=List[RecommendationResponse])
def get_recommendation_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's recommendation history."""
    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .order_by(Recommendation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return recommendations