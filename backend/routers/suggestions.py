"""
Suggestions router for AI-powered activity recommendations.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from database.database import get_db
from database.models import User, Activity, Suggestion, UserActivity
from schemas.schemas import (
    SuggestionResponse, SuggestionUpdate, ActivityResponse, ApiResponse
)
from auth.auth import get_current_active_user
from ai.suggestions import generate_suggestions, save_suggestions_to_db
from monitoring.logger import context_logger

router = APIRouter()


@router.get("/", response_model=List[SuggestionResponse])
async def get_user_suggestions(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(5, ge=1, le=20),
    fresh: bool = Query(False, description="Generate fresh suggestions instead of using cached ones"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized activity suggestions for the current user.
    
    Args:
        current_user: Current authenticated user
        limit: Number of suggestions to return
        fresh: Whether to generate fresh suggestions
        db: Database session
        
    Returns:
        List[SuggestionResponse]: Personalized suggestions
    """
    # Check for existing recent suggestions if not requesting fresh ones
    if not fresh:
        recent_suggestions = await get_recent_suggestions(current_user.id, limit, db)
        if recent_suggestions:
            context_logger.info(
                "Returning cached suggestions",
                user_id=current_user.id,
                suggestions_count=len(recent_suggestions)
            )
            return recent_suggestions
    
    # Generate new suggestions
    context_logger.info(
        "Generating fresh suggestions",
        user_id=current_user.id,
        limit=limit
    )
    
    # Get available activities (exclude ones user has already interacted with)
    user_activity_ids_result = await db.execute(
        select(UserActivity.activity_id)
        .where(UserActivity.user_id == current_user.id)
    )
    user_activity_ids = {row[0] for row in user_activity_ids_result.fetchall()}
    
    # Get activities excluding user's activities
    activities_query = select(Activity)
    if user_activity_ids:
        activities_query = activities_query.where(~Activity.id.in_(user_activity_ids))
    
    activities_result = await db.execute(activities_query.limit(50))  # Limit for performance
    activities = activities_result.scalars().all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No new activities available for suggestions"
        )
    
    # Generate AI suggestions
    try:
        suggestions_data = await generate_suggestions(current_user, activities, db, limit)
        
        # Create activities map for saving suggestions
        activities_map = {activity.id: activity for activity in activities}
        
        # Save suggestions to database
        saved_suggestions = await save_suggestions_to_db(
            current_user.id, suggestions_data, activities_map, db
        )
        
        # Return formatted suggestions
        response_suggestions = []
        for suggestion in saved_suggestions:
            activity = activities_map.get(suggestion.activity_id)
            if activity:
                response_suggestions.append(
                    SuggestionResponse(
                        id=suggestion.id,
                        activity=ActivityResponse.model_validate(activity),
                        score=suggestion.score,
                        reasons=suggestion.reasons,
                        viewed=suggestion.viewed,
                        clicked=suggestion.clicked,
                        dismissed=suggestion.dismissed,
                        created_at=suggestion.created_at,
                        expires_at=suggestion.expires_at
                    )
                )
        
        return response_suggestions
        
    except Exception as e:
        context_logger.error(
            "Failed to generate suggestions",
            user_id=current_user.id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate personalized suggestions"
        )


async def get_recent_suggestions(
    user_id: str,
    limit: int,
    db: AsyncSession
) -> List[SuggestionResponse]:
    """
    Get recent cached suggestions for a user.
    
    Args:
        user_id: User ID
        limit: Number of suggestions to return
        db: Database session
        
    Returns:
        List[SuggestionResponse]: Recent suggestions
    """
    from datetime import datetime, timedelta
    
    # Get suggestions from the last 24 hours that haven't been dismissed
    cutoff_time = datetime.utcnow() - timedelta(hours=24)
    
    suggestions_result = await db.execute(
        select(Suggestion)
        .options(selectinload(Suggestion.activity))
        .where(
            and_(
                Suggestion.user_id == user_id,
                Suggestion.created_at >= cutoff_time,
                Suggestion.dismissed == False
            )
        )
        .order_by(Suggestion.score.desc())
        .limit(limit)
    )
    suggestions = suggestions_result.scalars().all()
    
    if not suggestions:
        return []
    
    # Get associated activities
    activity_ids = [s.activity_id for s in suggestions]
    activities_result = await db.execute(
        select(Activity).where(Activity.id.in_(activity_ids))
    )
    activities = {a.id: a for a in activities_result.scalars().all()}
    
    # Build response
    response_suggestions = []
    for suggestion in suggestions:
        activity = activities.get(suggestion.activity_id)
        if activity:
            response_suggestions.append(
                SuggestionResponse(
                    id=suggestion.id,
                    activity=ActivityResponse.model_validate(activity),
                    score=suggestion.score,
                    reasons=suggestion.reasons,
                    viewed=suggestion.viewed,
                    clicked=suggestion.clicked,
                    dismissed=suggestion.dismissed,
                    created_at=suggestion.created_at,
                    expires_at=suggestion.expires_at
                )
            )
    
    return response_suggestions


@router.put("/{suggestion_id}", response_model=ApiResponse)
async def update_suggestion(
    suggestion_id: str,
    suggestion_data: SuggestionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a suggestion (mark as viewed, clicked, or dismissed).
    
    Args:
        suggestion_id: Suggestion ID
        suggestion_data: Suggestion update data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Update result
    """
    result = await db.execute(
        select(Suggestion).where(
            and_(
                Suggestion.id == suggestion_id,
                Suggestion.user_id == current_user.id
            )
        )
    )
    suggestion = result.scalar_one_or_none()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    # Update fields
    update_data = suggestion_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(suggestion, field, value)
    
    await db.commit()
    
    context_logger.info(
        "Suggestion updated",
        user_id=current_user.id,
        suggestion_id=suggestion_id,
        updates=update_data
    )
    
    return ApiResponse(
        success=True,
        message="Suggestion updated successfully"
    )


@router.delete("/{suggestion_id}", response_model=ApiResponse)
async def dismiss_suggestion(
    suggestion_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Dismiss a suggestion (mark as dismissed).
    
    Args:
        suggestion_id: Suggestion ID
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ApiResponse: Dismissal result
    """
    result = await db.execute(
        select(Suggestion).where(
            and_(
                Suggestion.id == suggestion_id,
                Suggestion.user_id == current_user.id
            )
        )
    )
    suggestion = result.scalar_one_or_none()
    
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Suggestion not found"
        )
    
    suggestion.dismissed = True
    await db.commit()
    
    context_logger.info(
        "Suggestion dismissed",
        user_id=current_user.id,
        suggestion_id=suggestion_id
    )
    
    return ApiResponse(
        success=True,
        message="Suggestion dismissed successfully"
    )


@router.get("/stats", response_model=dict)
async def get_suggestion_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get suggestion statistics for the current user.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        dict: Suggestion statistics
    """
    # Get suggestion counts
    total_result = await db.execute(
        select(func.count(Suggestion.id)).where(Suggestion.user_id == current_user.id)
    )
    total_suggestions = total_result.scalar()
    
    clicked_result = await db.execute(
        select(func.count(Suggestion.id)).where(
            and_(
                Suggestion.user_id == current_user.id,
                Suggestion.clicked == True
            )
        )
    )
    clicked_suggestions = clicked_result.scalar()
    
    dismissed_result = await db.execute(
        select(func.count(Suggestion.id)).where(
            and_(
                Suggestion.user_id == current_user.id,
                Suggestion.dismissed == True
            )
        )
    )
    dismissed_suggestions = dismissed_result.scalar()
    
    # Calculate click-through rate
    ctr = (clicked_suggestions / total_suggestions * 100) if total_suggestions > 0 else 0
    
    return {
        "total_suggestions": total_suggestions,
        "clicked_suggestions": clicked_suggestions,
        "dismissed_suggestions": dismissed_suggestions,
        "click_through_rate": round(ctr, 2),
        "pending_suggestions": total_suggestions - clicked_suggestions - dismissed_suggestions
    }