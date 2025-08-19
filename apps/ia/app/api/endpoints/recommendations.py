"""
AI recommendations API endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.core.security import get_current_active_user
from app.models.models import User, Activity
from app.schemas.schemas import (
    ActivitySuggestion,
    SuggestionRequest,
    APIResponse
)
from app.services.ai_service import ai_service

router = APIRouter()

@router.post("/suggest", response_model=List[ActivitySuggestion])
async def get_activity_suggestions(
    request: SuggestionRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered activity suggestions for the current user"""
    
    # Build user profile for AI
    user_profile = {
        "skills": request.skills or getattr(current_user, 'skills', []),
        "availability": request.availability or getattr(current_user, 'availability', []),
        "preferences": request.preferences or getattr(current_user, 'preferences', []),
        "location": current_user.location,
        "is_mfr_student": current_user.is_mfr_student
    }
    
    # Get active activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities available"
        )
    
    # Get AI recommendations
    suggestions = await ai_service.generate_recommendations(
        user_profile=user_profile,
        activities=activities,
        limit=request.limit
    )
    
    return suggestions

@router.get("/suggest/me", response_model=List[ActivitySuggestion])
async def get_my_suggestions(
    limit: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered activity suggestions for the current user based on their profile"""
    
    # Build user profile
    user_profile = {
        "skills": getattr(current_user, 'skills', []),
        "availability": getattr(current_user, 'availability', []),
        "preferences": getattr(current_user, 'preferences', []),
        "location": current_user.location,
        "is_mfr_student": current_user.is_mfr_student
    }
    
    # Get active activities
    activities = db.query(Activity).filter(Activity.is_active == True).all()
    
    if not activities:
        return []
    
    # Get AI recommendations
    suggestions = await ai_service.generate_recommendations(
        user_profile=user_profile,
        activities=activities,
        limit=limit
    )
    
    return suggestions

@router.get("/ai-status", response_model=APIResponse)
async def get_ai_status():
    """Check if AI service is available"""
    is_available = ai_service.is_available()
    
    return APIResponse(
        success=True,
        message="AI service status retrieved",
        data={
            "ai_available": is_available,
            "fallback_mode": not is_available
        }
    )