"""
Activity service for business logic operations.
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import Activity, User


class ActivityService:
    """Service for activity-related operations."""
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def filter_by_preferences(self, activities: List[Activity], preferences: Dict[str, Any]) -> List[Activity]:
        """Filter activities based on user preferences."""
        filtered_activities = activities
        
        if "preferred_categories" in preferences:
            preferred_categories = preferences["preferred_categories"]
            filtered_activities = [
                activity for activity in filtered_activities
                if activity.category in preferred_categories
            ]
        
        return filtered_activities
    
    def calculate_match_score(self, activity: Dict[str, Any], user_preferences: Dict[str, Any]) -> float:
        """Calculate how well an activity matches user preferences."""
        score = 0.0
        max_score = 0.0
        
        # Category match
        if "interests" in user_preferences:
            max_score += 0.4
            interests = user_preferences["interests"]
            if activity.get("category") in interests:
                score += 0.4
        
        # Difficulty level match
        if "skill_level" in user_preferences:
            max_score += 0.3
            if activity.get("difficulty_level") == user_preferences["skill_level"]:
                score += 0.3
        
        # Duration match
        if "preferred_duration" in user_preferences:
            max_score += 0.3
            preferred_duration = user_preferences["preferred_duration"]
            activity_duration = activity.get("duration_minutes", 0)
            if abs(activity_duration - preferred_duration) <= 30:
                score += 0.3
        
        return score / max_score if max_score > 0 else 0.0
    
    def get_recommendations(self, user_id: int, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get personalized activity recommendations for a user."""
        # Get all published activities
        activities = self.db_session.query(Activity).filter(
            Activity.is_published == True
        ).all()
        
        # Calculate match scores and sort by relevance
        recommendations = []
        for activity in activities:
            activity_dict = {
                "id": activity.id,
                "title": activity.title,
                "description": activity.description,
                "category": activity.category,
                "difficulty_level": activity.difficulty_level,
                "duration_minutes": activity.duration_minutes
            }
            
            match_score = self.calculate_match_score(activity_dict, user_preferences)
            activity_dict["match_score"] = match_score
            recommendations.append(activity_dict)
        
        # Sort by match score (descending)
        recommendations.sort(key=lambda x: x["match_score"], reverse=True)
        
        return recommendations