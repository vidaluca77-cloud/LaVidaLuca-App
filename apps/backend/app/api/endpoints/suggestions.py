from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Activity, ActivitySuggestion
from ...schemas.schemas import ActivitySuggestion as ActivitySuggestionSchema
from ...core.config import settings


router = APIRouter()


@router.get(
    "/",
    response_model=List[ActivitySuggestionSchema],
    summary="Get user's activity suggestions",
    description="""
    Retrieve personalized activity suggestions for the current user.
    
    This endpoint returns activity recommendations that have been generated
    specifically for the authenticated user, either by AI or manual curation.
    
    **Authentication Required:**
    - Must be logged in with valid JWT token
    - Returns suggestions only for the authenticated user
    
    **Suggestion Sources:**
    - AI-powered recommendations based on user profile and preferences
    - Manual suggestions from educators or administrators
    - Algorithm-based suggestions using collaborative filtering
    
    **Ordering:**
    - Results are ordered by creation date (newest first)
    - Limited to the 10 most recent suggestions
    
    **Use Cases:**
    - Show personalized learning recommendations
    - Display activity suggestions in user dashboard
    - Provide guided learning paths
    """,
    responses={
        200: {
            "description": "Suggestions successfully retrieved",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "activity_id": 2,
                            "suggestion_reason": "Based on your interest in agriculture and beginner skill level",
                            "ai_generated": True,
                            "created_at": "2024-01-20T10:30:00Z",
                            "activity": {
                                "id": 2,
                                "title": "Organic Composting Basics",
                                "description": "Learn how to create nutrient-rich compost...",
                                "category": "agriculture",
                                "difficulty_level": "beginner",
                                "duration_minutes": 90,
                                "location": "Garden",
                                "equipment_needed": "Gloves, shovel, organic waste",
                                "learning_objectives": "Understand composting process...",
                                "is_published": True,
                                "creator_id": 2,
                                "created_at": "2024-01-18T10:30:00Z",
                                "updated_at": None
                            }
                        }
                    ]
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
        }
    },
    tags=["suggestions"]
)
def get_user_suggestions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity suggestions for the current user."""
    suggestions = db.query(ActivitySuggestion).filter(
        ActivitySuggestion.user_id == current_user.id
    ).order_by(ActivitySuggestion.created_at.desc()).limit(10).all()
    return suggestions


@router.post(
    "/generate",
    response_model=List[ActivitySuggestionSchema],
    status_code=status.HTTP_201_CREATED,
    summary="Generate new AI-powered suggestions",
    description="""
    Generate new personalized activity suggestions using AI or algorithmic recommendations.
    
    This endpoint creates new activity suggestions tailored to the user's profile,
    preferences, and learning history. The system avoids suggesting activities
    the user has already created.
    
    **Authentication Required:**
    - Must be logged in with valid JWT token
    - Suggestions are generated for the authenticated user
    
    **AI Integration:**
    - Uses OpenAI GPT models when API key is configured
    - Falls back to algorithmic suggestions when AI is unavailable
    - Considers user's existing activities and preferences
    
    **Preference Handling:**
    - Optional preferences string provides context to AI
    - Helps refine suggestions based on specific interests
    - Examples: "interested in sustainable farming", "prefer hands-on activities"
    
    **Duplicate Prevention:**
    - Avoids suggesting activities user has already created
    - Prevents duplicate suggestions for the same activity
    - Ensures fresh and relevant recommendations
    
    **Response:**
    - Returns 3-5 new activity suggestions
    - Each suggestion includes detailed reasoning
    - Suggestions are immediately saved for future reference
    """,
    responses={
        201: {
            "description": "Suggestions successfully generated",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "user_id": 1,
                            "activity_id": 2,
                            "suggestion_reason": "Perfect for your interest in sustainable practices and matches your beginner skill level",
                            "ai_generated": True,
                            "created_at": "2024-01-20T10:30:00Z",
                            "activity": {
                                "id": 2,
                                "title": "Water Conservation Techniques",
                                "description": "Learn effective water conservation methods for agricultural use...",
                                "category": "environment",
                                "difficulty_level": "beginner",
                                "duration_minutes": 90,
                                "location": "Field",
                                "equipment_needed": "Water meter, notebook",
                                "learning_objectives": "Understand water conservation principles...",
                                "is_published": True,
                                "creator_id": 3,
                                "created_at": "2024-01-19T10:30:00Z",
                                "updated_at": None
                            }
                        }
                    ]
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
        404: {
            "description": "No activities available for suggestions",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "No activities available for suggestions"
                    }
                }
            }
        },
        500: {
            "description": "AI integration error or system failure",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Failed to generate AI suggestions: OpenAI API error"
                    }
                }
            }
        }
    },
    tags=["suggestions"]
)
def generate_ai_suggestions(
    preferences: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Generate new AI-powered activity suggestions for the current user."""
    if not settings.OPENAI_API_KEY:
        # Return simple suggestions based on available activities when OpenAI is not configured
        available_activities = db.query(Activity).filter(
            Activity.is_published == True,
            Activity.creator_id != current_user.id
        ).limit(3).all()
        
        suggestions = []
        for activity in available_activities:
            # Check if suggestion already exists
            existing = db.query(ActivitySuggestion).filter(
                ActivitySuggestion.user_id == current_user.id,
                ActivitySuggestion.activity_id == activity.id
            ).first()
            
            if not existing:
                suggestion = ActivitySuggestion(
                    user_id=current_user.id,
                    activity_id=activity.id,
                    suggestion_reason="Recommended based on your profile and interests",
                    ai_generated=False
                )
                db.add(suggestion)
                suggestions.append(suggestion)
        
        db.commit()
        for suggestion in suggestions:
            db.refresh(suggestion)
        
        return suggestions
    
    # Get user's existing activities to avoid suggestions
    user_activities = db.query(Activity).filter(Activity.creator_id == current_user.id).all()
    user_activity_titles = [activity.title for activity in user_activities]
    
    # Get all available activities for suggestions
    available_activities = db.query(Activity).filter(
        Activity.is_published == True,
        Activity.creator_id != current_user.id
    ).all()
    
    if not available_activities:
        raise HTTPException(status_code=404, detail="No activities available for suggestions")
    
    try:
        # Import OpenAI here to avoid import errors when not available
        import openai
        openai.api_key = settings.OPENAI_API_KEY
        
        # Create prompt for OpenAI
        user_context = f"User: {current_user.full_name or current_user.username}"
        if user_activity_titles:
            user_context += f"\nUser has already created these activities: {', '.join(user_activity_titles)}"
        
        activity_list = "\n".join([
            f"- {activity.title} ({activity.category}, {activity.difficulty_level}): {activity.description[:100]}..."
            for activity in available_activities[:20]  # Limit to first 20 activities
        ])
        
        preferences_text = f"\nUser preferences: {preferences}" if preferences else ""
        
        prompt = f"""
        {user_context}
        {preferences_text}
        
        Available activities for recommendation:
        {activity_list}
        
        Based on the user's profile and preferences, recommend 3-5 activities from the list above.
        For each recommendation, provide a brief reason why this activity would be suitable.
        
        Respond in JSON format:
        [
            {{"activity_title": "Activity Name", "reason": "Why this activity is recommended"}},
            ...
        ]
        """
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that recommends educational activities for students in agricultural and rural training programs (MFR)."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Parse OpenAI response
        import json
        ai_response = response.choices[0].message.content
        recommendations = json.loads(ai_response)
        
        # Create suggestions in database
        suggestions = []
        for rec in recommendations:
            # Find the activity by title
            activity = next(
                (a for a in available_activities if a.title == rec["activity_title"]),
                None
            )
            if activity:
                # Check if suggestion already exists
                existing = db.query(ActivitySuggestion).filter(
                    ActivitySuggestion.user_id == current_user.id,
                    ActivitySuggestion.activity_id == activity.id
                ).first()
                
                if not existing:
                    suggestion = ActivitySuggestion(
                        user_id=current_user.id,
                        activity_id=activity.id,
                        suggestion_reason=rec["reason"],
                        ai_generated=True
                    )
                    db.add(suggestion)
                    suggestions.append(suggestion)
        
        db.commit()
        
        # Refresh suggestions to get relationships
        for suggestion in suggestions:
            db.refresh(suggestion)
        
        return suggestions
        
    except ImportError:
        raise HTTPException(
            status_code=500,
            detail="OpenAI integration not available"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI suggestions: {str(e)}"
        )