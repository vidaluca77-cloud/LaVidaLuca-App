"""
Activity recommendation service
"""
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from ..models.models import Activity, UserProfile, ActivityRecommendation
from ..schemas.schemas import UserProfileBase, ActivityRecommendation as RecommendationSchema
from .openai_service import openai_service


class RecommendationService:
    """Service for generating activity recommendations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_recommendations(
        self, 
        user_profile: UserProfileBase, 
        limit: int = 5
    ) -> List[RecommendationSchema]:
        """
        Generate personalized activity recommendations.
        
        Args:
            user_profile: User profile data
            limit: Maximum number of recommendations
            
        Returns:
            List of activity recommendations with scores and explanations
        """
        # Get all activities from database
        activities = self.db.query(Activity).all()
        
        # Calculate matching scores
        activity_scores = self._calculate_matching_scores(user_profile, activities)
        
        # Sort by score and limit results
        sorted_activities = sorted(activity_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Get activities and scores
        recommended_activities = []
        scores_dict = {}
        
        for activity_id, (score, reasons) in sorted_activities:
            activity = next(a for a in activities if a.id == activity_id)
            recommended_activities.append(activity)
            scores_dict[activity_id] = score
        
        # Generate AI explanations
        ai_explanations = await openai_service.generate_recommendations_explanation(
            user_profile, recommended_activities, scores_dict
        )
        
        # Build recommendations
        recommendations = []
        for activity_id, (score, reasons) in sorted_activities:
            activity = next(a for a in activities if a.id == activity_id)
            
            recommendation = RecommendationSchema(
                activity=activity,
                score=score,
                reasons=reasons,
                ai_explanation=ai_explanations.get(activity_id)
            )
            recommendations.append(recommendation)
        
        return recommendations
    
    def _calculate_matching_scores(
        self, 
        profile: UserProfileBase, 
        activities: List[Activity]
    ) -> Dict[int, Tuple[int, List[str]]]:
        """
        Calculate matching scores between user profile and activities.
        
        Returns:
            Dict mapping activity_id to (score, reasons) tuple
        """
        scores = {}
        
        for activity in activities:
            score = 0
            reasons = []
            
            # Skills matching (high weight)
            if profile.skills and activity.skill_tags:
                common_skills = set(profile.skills) & set(activity.skill_tags)
                if common_skills:
                    skill_score = len(common_skills) * 20
                    score += skill_score
                    reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
            
            # Category preferences (high weight)
            if profile.preferences and activity.category in profile.preferences:
                score += 25
                category_names = {
                    'agri': 'Agriculture',
                    'transfo': 'Transformation',
                    'artisanat': 'Artisanat',
                    'nature': 'Environnement',
                    'social': 'Animation'
                }
                reasons.append(f"Catégorie préférée : {category_names.get(activity.category, activity.category)}")
            
            # Experience level matching
            experience_bonus = self._get_experience_bonus(profile.experience_level, activity)
            if experience_bonus > 0:
                score += experience_bonus
                reasons.append(self._get_experience_reason(profile.experience_level, activity))
            
            # Duration suitability
            if activity.duration_min <= 120:  # Activities under 2 hours
                score += 10
                reasons.append("Durée adaptée pour commencer")
            
            # Safety level consideration
            if activity.safety_level <= 2:
                score += 10
                if activity.safety_level == 1:
                    reasons.append("Activité sans risque particulier")
            
            # Availability matching (simplified - could be more sophisticated)
            if profile.availability:
                score += 15
                reasons.append("Compatible avec vos disponibilités")
            
            # Location bonus (if specified)
            if profile.location:
                score += 5
                reasons.append("Disponible dans votre région")
            
            # Ensure score is within bounds
            score = min(score, 100)
            
            scores[activity.id] = (score, reasons)
        
        return scores
    
    def _get_experience_bonus(self, experience_level: str, activity: Activity) -> int:
        """Calculate bonus points based on experience level and activity complexity."""
        if experience_level == "debutant":
            # Favor simpler activities with lower safety levels
            if activity.safety_level == 1 and activity.duration_min <= 90:
                return 15
            elif activity.safety_level <= 2:
                return 10
        elif experience_level == "intermediaire":
            # Balanced approach
            if activity.safety_level <= 2:
                return 12
            else:
                return 8
        elif experience_level == "avance":
            # Can handle more complex activities
            if activity.safety_level >= 2:
                return 15
            else:
                return 10
        
        return 5  # Default small bonus
    
    def _get_experience_reason(self, experience_level: str, activity: Activity) -> str:
        """Get explanation for experience-based recommendation."""
        if experience_level == "debutant":
            return "Adapté aux débutants"
        elif experience_level == "intermediaire":
            return "Correspond à votre niveau d'expérience"
        elif experience_level == "avance":
            return "Activité enrichissante pour votre niveau"
        return "Adapté à votre profil"