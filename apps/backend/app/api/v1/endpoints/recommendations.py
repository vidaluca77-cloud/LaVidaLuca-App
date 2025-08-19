from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import openai
import json
import logging

from ...core.database import get_db
from ...core.config import settings
from ...models.activity import Activity
from ...models.user import User
from ...schemas.activity import ActivityRecommendation, ActivityResponse
from .users import get_current_user

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize OpenAI
openai.api_key = settings.openai_api_key

def calculate_activity_match_score(user: User, activity: Activity) -> float:
    """Calculate compatibility score between user and activity"""
    score = 0.0
    max_score = 100.0
    
    # Skill matching (40% of score)
    user_skills = set(user.skills) if user.skills else set()
    activity_skills = set(activity.skill_tags) if activity.skill_tags else set()
    
    if activity_skills:
        skill_match = len(user_skills.intersection(activity_skills)) / len(activity_skills)
        score += skill_match * 40
    else:
        score += 20  # Neutral score if no skills specified
    
    # Category preference matching (30% of score)
    user_preferences = set(user.preferences) if user.preferences else set()
    if activity.category in user_preferences:
        score += 30
    elif not user_preferences:
        score += 15  # Neutral score if no preferences specified
    
    # Safety level vs user type (15% of score)
    if user.user_type == "mfr_student":
        # MFR students can handle higher safety levels
        safety_bonus = min(activity.safety_level * 5, 15)
        score += safety_bonus
    else:
        # General participants prefer lower safety levels
        safety_penalty = max(0, (activity.safety_level - 1) * 5)
        score += max(0, 15 - safety_penalty)
    
    # Duration vs availability (15% of score)
    if activity.duration_min <= 60:
        score += 15  # Short activities are generally preferred
    elif activity.duration_min <= 120:
        score += 10
    else:
        score += 5
    
    return min(score, max_score)

def get_recommendation_reasons(user: User, activity: Activity, score: float) -> List[str]:
    """Generate reasons for the recommendation"""
    reasons = []
    
    # Skill matching
    user_skills = set(user.skills) if user.skills else set()
    activity_skills = set(activity.skill_tags) if activity.skill_tags else set()
    matching_skills = user_skills.intersection(activity_skills)
    
    if matching_skills:
        reasons.append(f"Matches your skills: {', '.join(matching_skills)}")
    
    # Category preference
    if user.preferences and activity.category in user.preferences:
        category_names = {
            'agri': 'Agriculture',
            'transfo': 'Transformation',
            'artisanat': 'Artisanat',
            'nature': 'Environnement',
            'social': 'Animation'
        }
        reasons.append(f"Matches your interest in {category_names.get(activity.category, activity.category)}")
    
    # Duration
    if activity.duration_min <= 60:
        reasons.append("Short duration activity, perfect for trying something new")
    
    # Safety level
    if activity.safety_level == 1:
        reasons.append("Beginner-friendly activity with low safety requirements")
    
    # MFR specific
    if user.user_type == "mfr_student" and activity.is_mfr_only:
        reasons.append("Exclusive activity for MFR students")
    
    return reasons

async def get_ai_recommendations(user: User, activities: List[Activity]) -> str:
    """Get AI-powered recommendations using OpenAI"""
    if not settings.openai_api_key:
        logger.warning("OpenAI API key not configured, skipping AI recommendations")
        return "AI recommendations not available"
    
    try:
        # Prepare user profile for AI
        user_profile = {
            "skills": user.skills or [],
            "preferences": user.preferences or [],
            "user_type": user.user_type,
            "location": user.location
        }
        
        # Prepare activities summary
        activities_summary = []
        for activity in activities[:5]:  # Limit to top 5 for AI analysis
            activities_summary.append({
                "title": activity.title,
                "category": activity.category,
                "summary": activity.summary,
                "skills": activity.skill_tags,
                "duration": activity.duration_min
            })
        
        prompt = f"""
        Based on this user profile: {json.dumps(user_profile)}
        
        And these recommended activities: {json.dumps(activities_summary)}
        
        Provide a brief, encouraging message (2-3 sentences) explaining why these activities 
        would be great for this user. Focus on personal growth, skill development, and 
        connection to the La Vida Luca mission of sustainable agriculture and social insertion.
        
        Keep the tone warm, supportive, and motivating.
        """
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful mentor for the La Vida Luca project, helping young people discover meaningful agricultural and artisanal activities."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"Error getting AI recommendations: {e}")
        return "Découvrez ces activités qui correspondent à votre profil et à vos aspirations !"

@router.get("/", response_model=List[ActivityRecommendation])
async def get_recommendations(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations for the current user"""
    
    # Get all active activities
    query = db.query(Activity).filter(Activity.is_active == True)
    
    # Filter MFR-only activities for non-MFR users
    if current_user.user_type not in ["mfr_student", "educator", "admin"]:
        query = query.filter(Activity.is_mfr_only == False)
    
    activities = query.all()
    
    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities available"
        )
    
    # Calculate scores and create recommendations
    recommendations = []
    for activity in activities:
        score = calculate_activity_match_score(current_user, activity)
        reasons = get_recommendation_reasons(current_user, activity, score)
        match_percentage = int(score)
        
        recommendations.append(ActivityRecommendation(
            activity=ActivityResponse.model_validate(activity),
            score=score,
            reasons=reasons,
            match_percentage=match_percentage
        ))
    
    # Sort by score and limit results
    recommendations.sort(key=lambda x: x.score, reverse=True)
    recommendations = recommendations[:limit]
    
    return recommendations

@router.get("/ai-insights")
async def get_ai_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered insights about recommended activities"""
    
    # Get top recommendations
    query = db.query(Activity).filter(Activity.is_active == True)
    
    if current_user.user_type not in ["mfr_student", "educator", "admin"]:
        query = query.filter(Activity.is_mfr_only == False)
    
    activities = query.limit(5).all()
    
    if not activities:
        return {"message": "No activities available for analysis"}
    
    # Get AI recommendations
    ai_message = await get_ai_recommendations(current_user, activities)
    
    return {
        "message": ai_message,
        "activities_analyzed": len(activities)
    }