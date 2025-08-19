from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ...db.database import get_db
from ...api.deps import get_current_active_user
from ...models.models import User, Activity, ActivitySuggestion
from ...schemas.schemas import ActivitySuggestion as ActivitySuggestionSchema
from ...core.config import settings


router = APIRouter()


@router.get("/", response_model=List[ActivitySuggestionSchema], summary="Get user activity suggestions")
def get_user_suggestions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get personalized activity suggestions for the current user.
    
    **Authentication required.** Returns up to 10 of the most recent
    activity suggestions generated for the current user.
    
    Suggestions can be either:
    - AI-generated based on user preferences and profile
    - Simple recommendations based on available activities
    
    Each suggestion includes the recommended activity details and
    the reason why it was suggested.
    """
    suggestions = db.query(ActivitySuggestion).filter(
        ActivitySuggestion.user_id == current_user.id
    ).order_by(ActivitySuggestion.created_at.desc()).limit(10).all()
    return suggestions


@router.post("/generate", response_model=List[ActivitySuggestionSchema], summary="Generate new AI suggestions")
def generate_ai_suggestions(
    preferences: Optional[str] = Query(None, description="User preferences or interests to guide suggestions"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate new personalized activity suggestions using AI.
    
    **Authentication required.** This endpoint generates new activity
    suggestions based on the user's profile, existing activities, and
    optional preferences.
    
    **How it works:**
    1. If OpenAI is configured: Uses GPT to generate intelligent suggestions
       based on user context and available activities
    2. If OpenAI is not available: Returns simple recommendations based
       on available published activities
    
    **Parameters:**
    - **preferences**: Optional text describing user interests, goals,
      or specific areas they want to explore
    
    **Features:**
    - Avoids suggesting activities the user has already created
    - Only suggests from published activities
    - Stores suggestions in database for future reference
    - Prevents duplicate suggestions
    
    Returns a list of new suggestions with detailed reasoning.
    """
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