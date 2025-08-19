"""
Recommendation endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.security import get_current_active_user
from ...models.user import User
from ...models.activity import Activity
from ...models.recommendation import Recommendation
from ...schemas.recommendation import (
    Recommendation as RecommendationSchema,
    RecommendationCreate,
    RecommendationUpdate,
    RecommendationList,
    RecommendationRequest
)
from ...services.openai_service import openai_service

router = APIRouter()


@router.post("/generate", response_model=List[RecommendationSchema])
async def generate_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate AI-powered activity recommendations for the current user."""
    
    # Get active activities
    activities_query = db.query(Activity).filter(Activity.is_active == True)
    
    # Apply filters from request
    if request.preferred_difficulty:
        activities_query = activities_query.filter(
            Activity.difficulty_level <= request.preferred_difficulty + 1
        )
    
    if request.max_duration:
        activities_query = activities_query.filter(
            (Activity.duration_hours.is_(None)) | 
            (Activity.duration_hours <= request.max_duration)
        )
    
    activities = activities_query.all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found matching criteria"
        )
    
    # Generate recommendations using AI service
    ai_recommendations = await openai_service.generate_activity_recommendations(
        user=current_user,
        activities=activities,
        request=request,
        db=db
    )
    
    # Save recommendations to database
    saved_recommendations = []
    for ai_rec in ai_recommendations:
        # Check if recommendation already exists
        existing_rec = db.query(Recommendation).filter(
            Recommendation.user_id == current_user.id,
            Recommendation.activity_id == ai_rec["activity"].id
        ).first()
        
        if existing_rec:
            # Update existing recommendation
            existing_rec.confidence_score = ai_rec["confidence_score"]
            existing_rec.reasoning = ai_rec["reasoning"]
            existing_rec.recommendation_type = ai_rec["recommendation_type"]
            db.commit()
            db.refresh(existing_rec)
            saved_recommendations.append(existing_rec)
        else:
            # Create new recommendation
            db_recommendation = Recommendation(
                user_id=current_user.id,
                activity_id=ai_rec["activity"].id,
                confidence_score=ai_rec["confidence_score"],
                reasoning=ai_rec["reasoning"],
                recommendation_type=ai_rec["recommendation_type"]
            )
            db.add(db_recommendation)
            db.commit()
            db.refresh(db_recommendation)
            saved_recommendations.append(db_recommendation)
    
    return saved_recommendations


@router.get("/", response_model=RecommendationList)
async def get_user_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get recommendations for the current user."""
    query = db.query(Recommendation).filter(Recommendation.user_id == current_user.id)
    
    total = query.count()
    recommendations = query.offset(skip).limit(limit).all()
    
    return RecommendationList(
        recommendations=recommendations,
        total=total,
        page=skip // limit + 1,
        size=limit
    )


@router.get("/{recommendation_id}", response_model=RecommendationSchema)
async def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific recommendation."""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    # Check permissions
    if recommendation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return recommendation


@router.put("/{recommendation_id}", response_model=RecommendationSchema)
async def update_recommendation(
    recommendation_id: int,
    recommendation_update: RecommendationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a recommendation (for user feedback)."""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    # Check permissions
    if recommendation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update recommendation
    update_data = recommendation_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(recommendation, field, value)
    
    db.commit()
    db.refresh(recommendation)
    
    return recommendation


@router.delete("/{recommendation_id}")
async def delete_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a recommendation."""
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id
    ).first()
    
    if recommendation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found"
        )
    
    # Check permissions
    if recommendation.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    db.delete(recommendation)
    db.commit()
    
    return {"message": "Recommendation deleted successfully"}