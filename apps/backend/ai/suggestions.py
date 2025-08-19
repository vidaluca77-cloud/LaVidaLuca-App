"""
OpenAI integration for personalized activity suggestions.
Provides AI-powered recommendations based on user profiles and preferences.
"""

import openai
from typing import List, Dict, Any
from datetime import datetime
import os
from models import User, Activity
import schemas
import json
import asyncio
from database import settings

# Initialize OpenAI client
openai.api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")

def calculate_basic_score(user: User, activity: Activity) -> float:
    """Calculate a basic compatibility score without AI."""
    score = 0.5  # Base score
    
    user_profile = user.profile if user.profile else {}
    user_skills = user_profile.get("skills", [])
    user_interests = user_profile.get("interests", [])
    user_location = user_profile.get("location", "")
    user_experience = user_profile.get("experience_level", "beginner")
    
    # Skill matching
    if user_skills and activity.skill_tags:
        skill_matches = len(set(user_skills) & set(activity.skill_tags))
        total_skills = len(set(user_skills) | set(activity.skill_tags))
        if total_skills > 0:
            skill_score = skill_matches / total_skills
            score += skill_score * 0.3
    
    # Interest matching (if category matches interests)
    if user_interests and activity.category in user_interests:
        score += 0.2
    
    # Experience level matching
    experience_levels = {"beginner": 1, "intermediate": 3, "advanced": 5}
    user_exp_level = experience_levels.get(user_experience, 1)
    
    # Prefer activities that match or are slightly above user level
    if abs(activity.difficulty_level - user_exp_level) <= 1:
        score += 0.15
    elif activity.difficulty_level < user_exp_level:
        score += 0.1  # Slightly lower score for too easy activities
    
    # Location proximity (basic string matching)
    if user_location and activity.location:
        if user_location.lower() in activity.location.lower() or activity.location.lower() in user_location.lower():
            score += 0.1
    
    # Safety consideration
    if activity.safety_level <= 3:  # Prefer safer activities
        score += 0.05
    
    # Engagement and success rate
    score += activity.engagement_score * 0.1
    score += activity.success_rate * 0.1
    
    return min(score, 1.0)  # Cap at 1.0

def generate_basic_reasons(user: User, activity: Activity, score: float) -> List[str]:
    """Generate explanation reasons without AI."""
    reasons = []
    
    user_profile = user.profile if user.profile else {}
    user_skills = user_profile.get("skills", [])
    user_interests = user_profile.get("interests", [])
    user_location = user_profile.get("location", "")
    
    # Skill-based reasons
    if user_skills and activity.skill_tags:
        matching_skills = set(user_skills) & set(activity.skill_tags)
        if matching_skills:
            reasons.append(f"Matches your skills: {', '.join(list(matching_skills)[:3])}")
    
    # Interest-based reasons
    if user_interests and activity.category in user_interests:
        reasons.append(f"Aligns with your interest in {activity.category}")
    
    # Duration-based reasons
    if activity.duration_min <= 120:
        reasons.append("Quick activity that fits in your schedule")
    elif activity.duration_min <= 240:
        reasons.append("Moderate duration perfect for learning")
    
    # Safety considerations
    if activity.safety_level <= 2:
        reasons.append("Very safe activity suitable for beginners")
    elif activity.safety_level == 3:
        reasons.append("Well-balanced safety level")
    
    # Location-based reasons
    if user_location and activity.location:
        if user_location.lower() in activity.location.lower():
            reasons.append(f"Available in your area: {activity.location}")
    
    # Engagement reasons
    if activity.engagement_score > 0.7:
        reasons.append("Highly engaging activity loved by participants")
    elif activity.engagement_score > 0.5:
        reasons.append("Well-received activity with good feedback")
    
    # Default reasons if none generated
    if not reasons:
        reasons = [
            "Interesting educational activity",
            "Good for skill development",
            "Part of our curated selection"
        ]
    
    return reasons[:3]  # Limit to 3 reasons

async def get_ai_enhanced_suggestions(user: User, activities: List[Activity], preferences: Dict[str, Any], limit: int) -> schemas.SuggestionResponse:
    """Get AI-enhanced suggestions using OpenAI."""
    try:
        # Prepare user context for AI
        user_context = {
            "profile": user.profile,
            "preferences": preferences
        }
        
        # Prepare activities data for AI
        activities_data = []
        for activity in activities[:50]:  # Limit to avoid token limits
            activities_data.append({
                "id": activity.id,
                "title": activity.title,
                "category": activity.category,
                "summary": activity.summary,
                "skill_tags": activity.skill_tags,
                "duration_min": activity.duration_min,
                "safety_level": activity.safety_level,
                "difficulty_level": activity.difficulty_level
            })
        
        # Create OpenAI prompt
        prompt = f"""
        You are an AI assistant for La Vida Luca, a platform for young farmers education.
        
        User Profile: {json.dumps(user_context, indent=2)}
        
        Activities Available: {json.dumps(activities_data, indent=2)}
        
        Please recommend the top {limit} activities for this user and provide a compatibility score (0-1) 
        and reasons for each recommendation. Consider:
        - User's skills and interests
        - Activity difficulty vs user experience
        - Safety considerations
        - Educational value
        - Engagement potential
        
        Respond in JSON format:
        {{
            "recommendations": [
                {{
                    "activity_id": "activity_id",
                    "score": 0.85,
                    "reasons": ["reason1", "reason2", "reason3"]
                }}
            ]
        }}
        """
        
        # Call OpenAI API
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for educational activity recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        
        # Parse AI response
        ai_content = response.choices[0].message.content
        ai_recommendations = json.loads(ai_content)
        
        # Build suggestions from AI recommendations
        suggestions = []
        activity_dict = {activity.id: activity for activity in activities}
        
        for rec in ai_recommendations.get("recommendations", [])[:limit]:
            activity_id = rec.get("activity_id")
            if activity_id in activity_dict:
                activity = activity_dict[activity_id]
                suggestion = schemas.Suggestion(
                    activity=schemas.Activity.from_orm(activity),
                    score=rec.get("score", 0.5),
                    reasons=rec.get("reasons", ["AI recommended"])
                )
                suggestions.append(suggestion)
        
        return schemas.SuggestionResponse(
            suggestions=suggestions,
            total=len(suggestions),
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        # Fall back to basic suggestions if AI fails
        print(f"AI suggestions failed: {e}")
        return await get_basic_suggestions(user, activities, preferences, limit)

async def get_basic_suggestions(user: User, activities: List[Activity], preferences: Dict[str, Any], limit: int) -> schemas.SuggestionResponse:
    """Get basic suggestions without AI as fallback."""
    # Calculate scores for all activities
    scored_activities = []
    for activity in activities:
        score = calculate_basic_score(user, activity)
        reasons = generate_basic_reasons(user, activity, score)
        scored_activities.append((activity, score, reasons))
    
    # Sort by score and take top results
    scored_activities.sort(key=lambda x: x[1], reverse=True)
    top_activities = scored_activities[:limit]
    
    # Build suggestions
    suggestions = []
    for activity, score, reasons in top_activities:
        suggestion = schemas.Suggestion(
            activity=schemas.Activity.from_orm(activity),
            score=score,
            reasons=reasons
        )
        suggestions.append(suggestion)
    
    return schemas.SuggestionResponse(
        suggestions=suggestions,
        total=len(suggestions),
        generated_at=datetime.utcnow()
    )

async def get_ai_suggestions(user: User, activities: List[Activity], preferences: Dict[str, Any] = None, limit: int = 5) -> schemas.SuggestionResponse:
    """Get AI-powered activity suggestions with fallback to basic suggestions."""
    if not preferences:
        preferences = {}
    
    # Try AI-enhanced suggestions first if API key is available
    if openai.api_key:
        try:
            return await get_ai_enhanced_suggestions(user, activities, preferences, limit)
        except Exception as e:
            print(f"AI suggestions failed, falling back to basic: {e}")
    
    # Fall back to basic suggestions
    return await get_basic_suggestions(user, activities, preferences, limit)