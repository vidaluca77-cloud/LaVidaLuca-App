"""
OpenAI integration for generating personalized activity suggestions.
"""

import os
import json
import time
from typing import List, Dict, Any
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Activity, UserActivity, Suggestion
from schemas.schemas import SuggestionResponse, ActivityResponse
from monitoring.logger import context_logger
from monitoring.metrics import record_ai_request

# Initialize OpenAI client
openai_api_key = os.getenv("OPENAI_API_KEY")
client = None

if openai_api_key:
    client = AsyncOpenAI(api_key=openai_api_key)
else:
    context_logger.warning("OpenAI API key not provided - AI suggestions will be limited")


async def generate_suggestions(
    user: User,
    activities: List[Activity],
    db: AsyncSession,
    limit: int = 5
) -> List[Dict[str, Any]]:
    """
    Generate personalized activity suggestions for a user using OpenAI.
    
    Args:
        user: User to generate suggestions for
        activities: Available activities
        db: Database session
        limit: Maximum number of suggestions
        
    Returns:
        List[Dict]: List of suggestions with scores and reasons
    """
    start_time = time.time()
    
    try:
        # Get user's activity history
        user_activities_result = await db.execute(
            select(UserActivity).where(UserActivity.user_id == user.id)
        )
        user_activities = user_activities_result.scalars().all()
        
        # Build user profile context
        user_context = build_user_context(user, user_activities)
        
        # Build activities context
        activities_context = build_activities_context(activities)
        
        # Generate suggestions using OpenAI
        try:
            suggestions = await call_openai_for_suggestions(
                user_context, activities_context, limit
            )
        except (ValueError, Exception) as openai_error:
            context_logger.warning(
                "OpenAI generation failed, falling back to rule-based suggestions",
                user_id=user.id,
                error=str(openai_error)
            )
            # Fall back to rule-based suggestions
            suggestions = generate_fallback_suggestions(user, activities, limit)
        
        # Record successful AI request
        duration = time.time() - start_time
        record_ai_request("suggestions", duration, True)
        
        context_logger.info(
            "AI suggestions generated successfully",
            user_id=user.id,
            suggestions_count=len(suggestions),
            duration=duration
        )
        
        return suggestions
        
    except Exception as e:
        # Record failed AI request
        duration = time.time() - start_time
        record_ai_request("suggestions", duration, False)
        
        context_logger.error(
            "Failed to generate AI suggestions",
            user_id=user.id,
            error=str(e),
            duration=duration
        )
        
        # Fallback to simple rule-based suggestions
        return generate_fallback_suggestions(user, activities, limit)


def build_user_context(user: User, user_activities: List[UserActivity]) -> str:
    """
    Build user context string for AI prompt.
    
    Args:
        user: User object
        user_activities: User's activity history
        
    Returns:
        str: User context for AI prompt
    """
    context = f"""
User Profile:
- Skills: {', '.join(user.skills) if user.skills else 'None specified'}
- Availability: {', '.join(user.availability) if user.availability else 'Not specified'}
- Location: {user.location or 'Not specified'}
- Bio: {user.bio or 'Not provided'}

Activity History:
"""
    
    completed_activities = [ua for ua in user_activities if ua.interaction_type == "completed"]
    favorited_activities = [ua for ua in user_activities if ua.interaction_type == "favorited"]
    
    if completed_activities:
        context += f"- Completed {len(completed_activities)} activities\n"
        # Add details about recent completions with ratings
        recent_completions = sorted(completed_activities, key=lambda x: x.created_at, reverse=True)[:3]
        for ua in recent_completions:
            rating_text = f" (rated {ua.rating}/5)" if ua.rating else ""
            context += f"  - Activity ID: {ua.activity_id}{rating_text}\n"
    
    if favorited_activities:
        context += f"- Favorited {len(favorited_activities)} activities\n"
    
    return context.strip()


def build_activities_context(activities: List[Activity]) -> str:
    """
    Build activities context string for AI prompt.
    
    Args:
        activities: List of available activities
        
    Returns:
        str: Activities context for AI prompt
    """
    context = "Available Activities:\n"
    
    for activity in activities[:20]:  # Limit to avoid token limits
        context += f"""
Activity ID: {activity.id}
Title: {activity.title}
Category: {activity.category}
Summary: {activity.summary}
Duration: {activity.duration_min} minutes
Skills: {', '.join(activity.skill_tags) if activity.skill_tags else 'None'}
Safety Level: {activity.safety_level}/5
Materials: {', '.join(activity.materials[:3]) if activity.materials else 'None'}
Location: {activity.location_type or 'Any'}
Season: {', '.join(activity.season) if activity.season else 'Any'}
---
"""
    
    return context.strip()


async def call_openai_for_suggestions(
    user_context: str,
    activities_context: str,
    limit: int
) -> List[Dict[str, Any]]:
    """
    Call OpenAI API to generate suggestions.
    
    Args:
        user_context: User profile context
        activities_context: Activities context
        limit: Number of suggestions to generate
        
    Returns:
        List[Dict]: AI-generated suggestions
        
    Raises:
        ValueError: If OpenAI client is not available
    """
    if not client:
        raise ValueError("OpenAI client not initialized - API key required")
    
    prompt = f"""
You are an AI assistant for La Vida Luca, a platform for young people in rural France (MFR - Maisons Familiales Rurales) focused on agriculture and sustainable development.

Based on the user profile and available activities, suggest the {limit} most relevant activities for this user.

{user_context}

{activities_context}

For each suggestion, provide:
1. Activity ID (exactly as listed above)
2. Relevance score (0.0 to 1.0)
3. 2-3 brief reasons why this activity matches the user

Respond in valid JSON format:
[
  {{
    "activity_id": "activity_id_here",
    "score": 0.85,
    "reasons": ["reason 1", "reason 2", "reason 3"]
  }}
]

Consider:
- User's existing skills and interests
- Their availability and location
- Activity difficulty and safety level
- Variety in recommendations (different categories)
- Seasonal appropriateness
- Learning progression (building skills)
"""

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant that provides activity recommendations in JSON format."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    
    # Parse the JSON response
    content = response.choices[0].message.content.strip()
    
    try:
        suggestions = json.loads(content)
        return suggestions
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract JSON from the response
        import re
        json_match = re.search(r'\[.*\]', content, re.DOTALL)
        if json_match:
            suggestions = json.loads(json_match.group())
            return suggestions
        else:
            raise ValueError("Could not parse JSON response from OpenAI")


def generate_fallback_suggestions(
    user: User,
    activities: List[Activity],
    limit: int
) -> List[Dict[str, Any]]:
    """
    Generate fallback suggestions using simple rules when AI fails.
    
    Args:
        user: User object
        activities: Available activities
        limit: Number of suggestions to generate
        
    Returns:
        List[Dict]: Rule-based suggestions
    """
    suggestions = []
    
    # Score activities based on simple rules
    for activity in activities[:limit * 2]:  # Consider more activities than limit
        score = 0.5  # Base score
        reasons = []
        
        # Match skills
        if user.skills:
            skill_matches = set(user.skills) & set(activity.skill_tags)
            if skill_matches:
                score += 0.3
                reasons.append(f"Matches your skills: {', '.join(skill_matches)}")
        
        # Prefer safer activities for beginners
        if activity.safety_level <= 2:
            score += 0.1
            reasons.append("Safe and beginner-friendly")
        
        # Prefer shorter activities
        if activity.duration_min <= 120:
            score += 0.1
            reasons.append("Manageable duration")
        
        # Category variety bonus
        if not any(s["activity_id"] == activity.id for s in suggestions):
            suggestions.append({
                "activity_id": activity.id,
                "score": min(score, 1.0),
                "reasons": reasons or ["Recommended for exploration"]
            })
    
    # Sort by score and return top suggestions
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return suggestions[:limit]


async def save_suggestions_to_db(
    user_id: str,
    suggestions: List[Dict[str, Any]],
    activities_map: Dict[str, Activity],
    db: AsyncSession
) -> List[Suggestion]:
    """
    Save generated suggestions to the database.
    
    Args:
        user_id: User ID
        suggestions: Generated suggestions
        activities_map: Map of activity IDs to Activity objects
        db: Database session
        
    Returns:
        List[Suggestion]: Saved suggestion objects
    """
    saved_suggestions = []
    
    for suggestion in suggestions:
        activity_id = suggestion["activity_id"]
        
        if activity_id not in activities_map:
            continue
        
        db_suggestion = Suggestion(
            user_id=user_id,
            activity_id=activity_id,
            score=suggestion["score"],
            reasons=suggestion["reasons"],
            ai_model="gpt-3.5-turbo"
        )
        
        db.add(db_suggestion)
        saved_suggestions.append(db_suggestion)
    
    await db.commit()
    
    # Refresh objects
    for suggestion in saved_suggestions:
        await db.refresh(suggestion)
    
    return saved_suggestions