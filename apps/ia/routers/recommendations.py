from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from database.models import User, Activity, Recommendation
from schemas.recommendation import (
    Suggestion, RecommendationRequest, 
    Recommendation as RecommendationSchema,
    RecommendationCreate
)
from schemas.user import UserProfile
from auth.security import get_current_active_user
from services.recommendation import recommendation_service

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/suggest", response_model=List[Suggestion])
async def get_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered activity recommendations based on user profile"""
    
    # Convert request profile to UserProfile
    user_profile = UserProfile(**request.user_profile)
    
    # Get all activities
    activities = db.query(Activity).all()
    
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")
    
    # Get AI recommendations
    suggestions = await recommendation_service.get_ai_recommendations(
        user_profile=user_profile,
        activities=activities,
        limit=request.limit
    )
    
    return suggestions


@router.get("/me", response_model=List[RecommendationSchema])
def get_my_recommendations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get saved recommendations for the current user"""
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == current_user.id
    ).order_by(Recommendation.created_at.desc()).limit(20).all()
    
    return recommendations


@router.post("/save", response_model=RecommendationSchema)
def save_recommendation(
    recommendation: RecommendationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Save a recommendation for the current user"""
    
    # Verify activity exists
    activity = db.query(Activity).filter(Activity.id == recommendation.activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    # Create recommendation
    db_recommendation = Recommendation(
        user_id=current_user.id,
        activity_id=recommendation.activity_id,
        score=recommendation.score,
        reasons=recommendation.reasons,
        ai_generated=recommendation.ai_generated
    )
    
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    
    return db_recommendation


@router.post("/generate", response_model=List[Suggestion])
async def generate_recommendations_for_user(
    limit: int = 5,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate AI recommendations for the current authenticated user"""
    
    # Create user profile from current user data
    user_profile = UserProfile(
        skills=current_user.skills or [],
        availability=current_user.availability or [],
        location=current_user.location or "",
        preferences=current_user.preferences or []
    )
    
    # Get all activities
    activities = db.query(Activity).all()
    
    if not activities:
        raise HTTPException(status_code=404, detail="No activities found")
    
    # Get AI recommendations
    suggestions = await recommendation_service.get_ai_recommendations(
        user_profile=user_profile,
        activities=activities,
        limit=limit
    )
    
    # Optionally save the recommendations
    for suggestion in suggestions:
        db_recommendation = Recommendation(
            user_id=current_user.id,
            activity_id=suggestion.activity.id,
            score=suggestion.score,
            reasons=suggestion.reasons,
            ai_generated=True
        )
        db.add(db_recommendation)
    
    db.commit()
    
    return suggestions


@router.delete("/{recommendation_id}")
def delete_recommendation(
    recommendation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a recommendation"""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == current_user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    db.delete(recommendation)
    db.commit()
    
    return {"message": "Recommendation deleted successfully"}