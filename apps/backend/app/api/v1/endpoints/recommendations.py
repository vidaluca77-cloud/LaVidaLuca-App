from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import json

from app.core.database import get_db
from app.core.config import settings
from app.models import Activity as ActivityModel, User as UserModel
from app.schemas import ActivityRecommendation
from .users import get_current_active_user
from openai import OpenAI

router = APIRouter()


def get_openai_client():
    """Get OpenAI client with API key from settings"""
    try:
        return OpenAI(api_key=settings.OPENAI_API_KEY)
    except Exception:
        return None


def get_user_activity_history(db: Session, user_id: int) -> List[ActivityModel]:
    """Get activities the user might have participated in or shown interest in"""
    # For now, we'll simulate this. In a real app, you'd have a participation/interest table
    # This is a placeholder that returns recent activities as "user history"
    return db.query(ActivityModel).filter(
        ActivityModel.is_active == True
    ).limit(5).all()


def generate_activity_recommendations(
    user: UserModel, 
    user_activities: List[ActivityModel],
    all_activities: List[ActivityModel]
) -> List[dict]:
    """Use OpenAI to generate personalized activity recommendations"""
    
    # Prepare context for OpenAI
    user_context = {
        "level": user.level or "unknown",
        "school": user.school or "unknown",
        "location": user.location or "unknown",
        "bio": user.bio or "No bio provided",
        "past_activities": [
            {
                "title": activity.title,
                "category": activity.category.value,
                "difficulty": activity.difficulty.value
            }
            for activity in user_activities[:3]  # Last 3 activities
        ]
    }
    
    available_activities = [
        {
            "id": activity.id,
            "title": activity.title,
            "category": activity.category.value,
            "difficulty": activity.difficulty.value,
            "description": activity.description[:200] + "..." if len(activity.description) > 200 else activity.description
        }
        for activity in all_activities[:20]  # Limit to 20 for context size
    ]
    
    prompt = f"""
    You are an AI assistant for "La Vida Luca", a platform for MFR (Maison Familiale Rurale) students 
    to discover agricultural, artisanal, and environmental activities.
    
    User Profile:
    - Level: {user_context['level']}
    - School: {user_context['school']}
    - Location: {user_context['location']}
    - Bio: {user_context['bio']}
    - Past Activities: {json.dumps(user_context['past_activities'], indent=2)}
    
    Available Activities:
    {json.dumps(available_activities, indent=2)}
    
    Based on the user's profile and past activities, recommend 3-5 activities that would be most 
    beneficial for their learning journey. Consider:
    - Progressive difficulty based on their experience
    - Complementary skills to their past activities
    - Regional relevance if location is known
    - Educational value for MFR context
    
    Return ONLY a JSON array with this structure:
    [
        {{
            "activity_id": int,
            "activity_title": "string",
            "reason": "string explaining why this is recommended",
            "confidence_score": float (0.0 to 1.0),
            "recommended_next_steps": "string with actionable advice"
        }}
    ]
    """
    
    try:
        client = get_openai_client()
        if not client:
            raise Exception("OpenAI client not available")
            
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an educational advisor for agricultural and rural training programs."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Parse the JSON response
        recommendations_text = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if recommendations_text.startswith("```"):
            recommendations_text = recommendations_text.split("```")[1]
            if recommendations_text.startswith("json"):
                recommendations_text = recommendations_text[4:]
        
        recommendations = json.loads(recommendations_text)
        return recommendations
        
    except Exception as e:
        # Fallback to simple recommendation logic if OpenAI fails
        print(f"OpenAI recommendation failed: {e}")
        return generate_fallback_recommendations(user, user_activities, all_activities)


def generate_fallback_recommendations(
    user: UserModel,
    user_activities: List[ActivityModel], 
    all_activities: List[ActivityModel]
) -> List[dict]:
    """Fallback recommendation logic when OpenAI is unavailable"""
    
    # Simple logic: recommend activities from different categories
    user_categories = set(activity.category for activity in user_activities)
    recommendations = []
    
    for activity in all_activities[:10]:
        if activity.category not in user_categories:
            recommendations.append({
                "activity_id": activity.id,
                "activity_title": activity.title,
                "reason": f"Diversify your skills with {activity.category.value} activities",
                "confidence_score": 0.7,
                "recommended_next_steps": f"Start with the basics of {activity.title} and gradually build your skills"
            })
            
            if len(recommendations) >= 3:
                break
    
    return recommendations


@router.get("/", response_model=List[ActivityRecommendation])
def get_activity_recommendations(
    limit: int = Query(5, description="Number of recommendations to return"),
    current_user: UserModel = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations for the current user"""
    
    # Get user's activity history
    user_activities = get_user_activity_history(db, current_user.id)
    
    # Get all available activities
    all_activities = db.query(ActivityModel).filter(
        ActivityModel.is_active == True
    ).all()
    
    if not all_activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities available for recommendations"
        )
    
    # Generate recommendations using OpenAI
    try:
        recommendations_data = generate_activity_recommendations(
            current_user, user_activities, all_activities
        )
        
        # Validate and format recommendations
        recommendations = []
        for rec_data in recommendations_data[:limit]:
            # Verify activity exists
            activity = db.query(ActivityModel).filter(
                ActivityModel.id == rec_data["activity_id"],
                ActivityModel.is_active == True
            ).first()
            
            if activity:
                recommendations.append(ActivityRecommendation(
                    activity_id=rec_data["activity_id"],
                    activity_title=rec_data["activity_title"],
                    reason=rec_data["reason"],
                    confidence_score=rec_data["confidence_score"],
                    recommended_next_steps=rec_data.get("recommended_next_steps")
                ))
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.get("/similar/{activity_id}", response_model=List[ActivityRecommendation])
def get_similar_activities(
    activity_id: int,
    limit: int = Query(3, description="Number of similar activities to return"),
    db: Session = Depends(get_db)
):
    """Get activities similar to the specified activity"""
    
    # Get the reference activity
    reference_activity = db.query(ActivityModel).filter(
        ActivityModel.id == activity_id,
        ActivityModel.is_active == True
    ).first()
    
    if not reference_activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    # Find similar activities (same category or difficulty)
    similar_activities = db.query(ActivityModel).filter(
        ActivityModel.is_active == True,
        ActivityModel.id != activity_id,
        (
            (ActivityModel.category == reference_activity.category) |
            (ActivityModel.difficulty == reference_activity.difficulty)
        )
    ).limit(limit * 2).all()  # Get more to filter better matches
    
    recommendations = []
    for activity in similar_activities[:limit]:
        similarity_reason = []
        
        if activity.category == reference_activity.category:
            similarity_reason.append(f"same category ({activity.category.value})")
        
        if activity.difficulty == reference_activity.difficulty:
            similarity_reason.append(f"same difficulty level ({activity.difficulty.value})")
        
        reason = f"Similar to '{reference_activity.title}': " + " and ".join(similarity_reason)
        
        recommendations.append(ActivityRecommendation(
            activity_id=activity.id,
            activity_title=activity.title,
            reason=reason,
            confidence_score=0.8,
            recommended_next_steps=f"If you enjoyed '{reference_activity.title}', you'll likely find '{activity.title}' engaging as well"
        ))
    
    return recommendations


@router.get("/trending/", response_model=List[ActivityRecommendation])
def get_trending_activities(
    limit: int = Query(5, description="Number of trending activities to return"),
    db: Session = Depends(get_db)
):
    """Get trending/popular activities (placeholder implementation)"""
    
    # For now, return featured activities as "trending"
    # In a real implementation, you'd track user engagement metrics
    trending_activities = db.query(ActivityModel).filter(
        ActivityModel.is_active == True,
        ActivityModel.is_featured == True
    ).limit(limit).all()
    
    if not trending_activities:
        # Fallback to recent activities
        trending_activities = db.query(ActivityModel).filter(
            ActivityModel.is_active == True
        ).order_by(ActivityModel.created_at.desc()).limit(limit).all()
    
    recommendations = []
    for activity in trending_activities:
        recommendations.append(ActivityRecommendation(
            activity_id=activity.id,
            activity_title=activity.title,
            reason="Currently trending among MFR students",
            confidence_score=0.9,
            recommended_next_steps="Join the community exploring this popular activity"
        ))
    
    return recommendations