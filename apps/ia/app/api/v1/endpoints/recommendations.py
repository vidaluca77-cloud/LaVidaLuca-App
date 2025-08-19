"""
Recommendations endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.models import User, Activity, Recommendation, UserProfile
from app.schemas.schemas import (
    RecommendationRequest,
    RecommendationResponse,
    Recommendation as RecommendationSchema,
    RecommendationCreate
)
from app.services.openai_service import openai_service

router = APIRouter()


@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered recommendations for the current user
    """
    # Get available activities with optional filtering
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if request.category_filter:
        query = query.filter(Activity.category.in_([cat.value for cat in request.category_filter]))
    
    if request.difficulty_filter:
        query = query.filter(Activity.difficulty_level.in_([diff.value for diff in request.difficulty_filter]))
    
    available_activities = query.all()
    
    if not available_activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities available with the specified filters"
        )
    
    # Generate recommendations using OpenAI service
    ai_recommendations = await openai_service.generate_recommendations(
        user_profile=request.user_profile,
        available_activities=available_activities,
        max_recommendations=request.max_recommendations
    )
    
    # Save recommendations to database
    saved_recommendations = []
    for rec_data in ai_recommendations:
        # Delete existing recommendation for this user-activity pair
        existing = db.query(Recommendation).filter(
            Recommendation.user_id == current_user.id,
            Recommendation.activity_id == rec_data["activity_id"]
        ).first()
        if existing:
            db.delete(existing)
        
        # Create new recommendation
        recommendation = Recommendation(
            user_id=current_user.id,
            activity_id=rec_data["activity_id"],
            score=rec_data["score"],
            reasons=rec_data["reasons"],
            ai_explanation=rec_data["ai_explanation"]
        )
        
        db.add(recommendation)
        db.flush()  # Get the ID
        db.refresh(recommendation)
        
        # Add activity data to response
        recommendation.activity = rec_data["activity"]
        saved_recommendations.append(recommendation)
    
    db.commit()
    
    return RecommendationResponse(
        recommendations=saved_recommendations,
        total_count=len(saved_recommendations),
        generated_at=datetime.utcnow()
    )


@router.get("/", response_model=List[RecommendationSchema])
async def get_user_recommendations(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get saved recommendations for the current user
    """
    recommendations = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .order_by(Recommendation.score.desc(), Recommendation.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    
    return recommendations


@router.get("/activity/{activity_id}", response_model=RecommendationSchema)
async def get_recommendation_for_activity(
    activity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get recommendation for a specific activity
    """
    recommendation = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == current_user.id,
            Recommendation.activity_id == activity_id
        )
        .first()
    )
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No recommendation found for this activity"
        )
    
    return recommendation


@router.delete("/{recommendation_id}")
async def delete_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete a specific recommendation
    """
    recommendation = (
        db.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.user_id == current_user.id
        )
        .first()
    )
    
    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    db.delete(recommendation)
    db.commit()
    
    return {"message": "Recommendation deleted successfully"}


@router.delete("/")
async def clear_all_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Clear all recommendations for the current user
    """
    deleted_count = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == current_user.id)
        .delete()
    )
    
    db.commit()
    
    return {"message": f"Deleted {deleted_count} recommendations"}


@router.post("/quick", response_model=RecommendationResponse)
async def quick_recommendations(
    max_recommendations: int = 3,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Quick recommendations based on user's saved profile
    """
    # Get user's profile
    user_profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.id).first()
    
    if not user_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found. Please create a profile first."
        )
    
    # Convert to UserProfileBase for the request
    from app.schemas.schemas import UserProfileBase
    profile_data = UserProfileBase(
        skills=user_profile.skills or [],
        availability=user_profile.availability or [],
        location=user_profile.location,
        preferences=user_profile.preferences or [],
        bio=user_profile.bio,
        mfr_level=user_profile.mfr_level,
        age_range=user_profile.age_range
    )
    
    # Create recommendation request
    request = RecommendationRequest(
        user_profile=profile_data,
        max_recommendations=max_recommendations
    )
    
    # Generate recommendations
    return await generate_recommendations(request, current_user, db)