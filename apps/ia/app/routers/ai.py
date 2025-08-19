from typing import List
from fastapi import APIRouter, HTTPException, status
from app.models import Suggestion, SuggestionRequest, Activity, UserProfile
from app.database import get_supabase_client

router = APIRouter(prefix="/ai", tags=["ai"])

def calculate_matching_score(activity: Activity, profile: UserProfile) -> tuple[float, List[str]]:
    """Calculate matching score between an activity and user profile."""
    score = 0.0
    reasons = []
    
    # Skills matching (weight: 15 points per skill)
    common_skills = [skill for skill in activity.skill_tags if skill in profile.skills]
    if common_skills:
        skill_score = len(common_skills) * 15
        score += skill_score
        reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
    
    # Category preference (weight: 25 points)
    if activity.category in profile.preferences:
        score += 25
        reasons.append(f"Catégorie préférée : {activity.category}")
    
    # Availability matching (weight: 10 points)
    # Simple availability check - could be enhanced with actual scheduling
    if profile.availability:
        score += 10
        reasons.append("Disponibilité compatible")
    
    # Duration preference (weight: 5-10 points based on duration)
    if activity.duration_min <= 90:
        score += 10
        reasons.append("Durée courte et accessible")
    elif activity.duration_min <= 150:
        score += 5
        reasons.append("Durée modérée")
    
    # Safety level bonus for beginners (fewer skills = higher safety preference)
    if len(profile.skills) < 3 and activity.safety_level <= 2:
        score += 15
        reasons.append("Activité sécurisée pour débuter")
    
    # Location bonus (simplified - in real implementation would use proper geo-matching)
    if profile.location:
        score += 5
        reasons.append("Localisation prise en compte")
    
    return score, reasons

@router.post("/suggestions", response_model=List[Suggestion])
async def get_activity_suggestions(request: SuggestionRequest):
    """Get AI-powered activity suggestions based on user profile."""
    supabase = get_supabase_client()
    
    try:
        # Fetch all activities
        response = supabase.table("activities").select("*").execute()
        activities = [Activity(**activity) for activity in response.data]
        
        # Calculate suggestions
        suggestions = []
        for activity in activities:
            score, reasons = calculate_matching_score(activity, request.profile)
            if score > 0:  # Only include activities with some matching
                suggestions.append(Suggestion(
                    activity=activity,
                    score=score,
                    reasons=reasons
                ))
        
        # Sort by score (descending) and return top suggestions
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:10]  # Return top 10 suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate suggestions: {str(e)}"
        )

@router.get("/categories")
async def get_activity_categories():
    """Get available activity categories with counts."""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("activities").select("category").execute()
        
        # Count activities by category
        category_counts = {}
        for activity in response.data:
            category = activity["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            "categories": [
                {"id": "agri", "name": "Agriculture", "count": category_counts.get("agri", 0)},
                {"id": "transfo", "name": "Transformation", "count": category_counts.get("transfo", 0)},
                {"id": "artisanat", "name": "Artisanat", "count": category_counts.get("artisanat", 0)},
                {"id": "nature", "name": "Environnement", "count": category_counts.get("nature", 0)},
                {"id": "social", "name": "Animation", "count": category_counts.get("social", 0)},
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch categories: {str(e)}"
        )

@router.get("/skills")
async def get_available_skills():
    """Get all available skills from activities."""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("activities").select("skill_tags").execute()
        
        # Collect all unique skills
        all_skills = set()
        for activity in response.data:
            if activity["skill_tags"]:
                all_skills.update(activity["skill_tags"])
        
        return {"skills": sorted(list(all_skills))}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch skills: {str(e)}"
        )