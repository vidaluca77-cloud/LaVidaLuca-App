"""
AI-powered activity suggestions routes using OpenAI integration.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import Field
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


@router.post(
    "/", 
    response_model=ApiResponse[List[dict]],
    summary="Get personalized AI-powered activity suggestions",
    description="Generate personalized activity recommendations using AI based on user profile and preferences.",
    responses={
        200: {
            "description": "Suggestions generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": [
                            {
                                "activity": {
                                    "id": "uuid-string",
                                    "title": "Urban Gardening Workshop",
                                    "category": "agriculture",
                                    "difficulty_level": "beginner"
                                },
                                "score": 0.95,
                                "reasons": [
                                    "Matches your interest in sustainable living",
                                    "Beginner-friendly level suits your experience"
                                ]
                            }
                        ],
                        "message": "Suggestions generated successfully"
                    }
                }
            }
        },
        401: {
            "description": "Authentication required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Not authenticated"
                    }
                }
            }
        },
        503: {
            "description": "AI service unavailable",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "AI suggestions service is not available"
                    }
                }
            }
        }
    },
    tags=["AI Suggestions"]
)
async def get_personalized_suggestions(
    request: SuggestionRequest = Field(
        ...,
        example={
            "request": "I want to learn about sustainable farming techniques suitable for beginners",
            "max_suggestions": 5
        }
    ),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get personalized activity suggestions using AI.
    
    This endpoint uses OpenAI to generate personalized activity recommendations
    based on the user's profile, preferences, and current request. The AI analyzes
    available activities and matches them with user interests.
    
    **Authentication Required:** Bearer Token
    **Rate Limit:** 10 requests per hour per user
    **AI Service:** OpenAI GPT integration
    """
    if not settings.OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI suggestions service is not available"
        )
    
    try:
        # Get user's profile for personalization
        user_profile = current_user.profile or {}
        
        # Get available activities from database
        activities_result = await db.execute(
            select(Activity).where(Activity.is_published == True)
        )
        activities = activities_result.scalars().all()
        
        # Generate suggestions using OpenAI
        suggestions = await get_activity_suggestions(
            user_profile=user_profile,
            user_request=request.request,
            available_activities=[activity.to_dict() for activity in activities],
            max_suggestions=request.max_suggestions
        )
        
        return ApiResponse(
            success=True,
            data=suggestions,
            message="Suggestions generated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )


@router.get(
    "/featured", 
    response_model=ApiResponse[List[dict]],
    summary="Get featured activity suggestions",
    description="Retrieve featured activities as suggestions without requiring authentication.",
    responses={
        200: {
            "description": "Featured suggestions retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": [
                            {
                                "activity": {
                                    "id": "uuid-string",
                                    "title": "Community Garden Project",
                                    "category": "agriculture",
                                    "is_featured": True
                                },
                                "score": 1.0,
                                "reasons": [
                                    "Activité mise en avant",
                                    "Recommandée par l'équipe La Vida Luca"
                                ]
                            }
                        ],
                        "message": "Featured suggestions retrieved successfully"
                    }
                }
            }
        }
    },
    tags=["AI Suggestions"]
)
async def get_featured_suggestions(
    limit: int = Query(
        5, 
        ge=1, 
        le=20, 
        description="Number of featured activities to return"
    ),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get featured activities as suggestions (no authentication required).
    
    This endpoint returns activities that have been marked as featured
    by the platform administrators. These represent high-quality, recommended
    learning experiences.
    
    **No Authentication Required**
    **Rate Limit:** 100 requests per minute per IP
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


@router.get(
    "/similar/{activity_id}", 
    response_model=ApiResponse[List[dict]],
    summary="Get similar activities",
    description="Find activities similar to a specific activity based on category, tags, and characteristics.",
    responses={
        200: {
            "description": "Similar activities retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "success": True,
                        "data": [
                            {
                                "activity": {
                                    "id": "uuid-string",
                                    "title": "Advanced Gardening Techniques",
                                    "category": "agriculture",
                                    "skill_tags": ["gardening", "sustainability"]
                                },
                                "score": 0.8,
                                "reasons": [
                                    "Même catégorie: agriculture",
                                    "Compétences similaires: gardening, sustainability"
                                ]
                            }
                        ],
                        "message": "Similar activities retrieved successfully"
                    }
                }
            }
        },
        404: {
            "description": "Activity not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Activity not found"
                    }
                }
            }
        }
    },
    tags=["AI Suggestions"]
)
async def get_similar_activities(
    activity_id: str = Field(..., description="ID of the reference activity"),
    limit: int = Query(
        5, 
        ge=1, 
        le=10, 
        description="Maximum number of similar activities to return"
    ),
    db: AsyncSession = Depends(get_db_session)
):
    """
    Get activities similar to a specific activity.
    
    This endpoint analyzes a given activity and returns similar activities
    based on category, skill tags, difficulty level, and other characteristics.
    The similarity score indicates how closely related each activity is.
    
    **No Authentication Required**
    **Rate Limit:** 50 requests per minute per IP
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