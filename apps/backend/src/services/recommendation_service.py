from typing import List, Optional
from sqlalchemy.orm import Session
from ..db import models, schemas

class ActivityRecommendationService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_recommendations(
        self, 
        user_id: int, 
        category_filter: Optional[str] = None,
        limit: int = 10
    ) -> List[schemas.ActivityRecommendation]:
        """
        Get activity recommendations for a user based on their profile and preferences.
        """
        # Get user and their profile
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return []
        
        # Get activities (filter by category if specified)
        query = self.db.query(models.Activity).filter(models.Activity.is_active == True)
        
        if category_filter:
            query = query.filter(models.Activity.category == category_filter)
        
        # Filter student-only activities for non-students
        if not user.is_student:
            query = query.filter(models.Activity.is_student_only == False)
        
        activities = query.all()
        
        # Get user's completed activities
        completed_activity_ids = set()
        completed_query = self.db.query(models.user_activities.c.activity_id).filter(
            models.user_activities.c.user_id == user_id
        )
        for result in completed_query:
            completed_activity_ids.add(result[0])
        
        # Calculate scores for each activity
        recommendations = []
        for activity in activities:
            # Skip completed activities
            if activity.id in completed_activity_ids:
                continue
                
            score, reasons = self._calculate_activity_score(user, activity)
            
            if score > 0:  # Only include activities with positive scores
                recommendations.append(schemas.ActivityRecommendation(
                    activity=schemas.Activity.from_orm(activity),
                    score=score,
                    reasons=reasons
                ))
        
        # Sort by score descending and limit results
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]
    
    def _calculate_activity_score(self, user: models.User, activity: models.Activity) -> tuple[float, List[str]]:
        """
        Calculate recommendation score for an activity based on user profile.
        Returns (score, reasons) tuple.
        """
        score = 0.0
        reasons = []
        
        # Base score for all activities
        score += 10.0
        
        # Category preference bonus
        if user.preferences and activity.category in user.preferences:
            score += 25.0
            reasons.append(f"Vous avez exprimé un intérêt pour la catégorie {activity.category}")
        
        # Skill matching bonus
        user_skill_names = [skill.name for skill in user.skills]
        activity_skill_names = [skill.name for skill in activity.required_skills]
        common_skills = set(user_skill_names) & set(activity_skill_names)
        
        if common_skills:
            skill_bonus = len(common_skills) * 15.0
            score += skill_bonus
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Duration preference (prefer activities 60-120 minutes for beginners)
        if 60 <= activity.duration_min <= 120:
            score += 10.0
            reasons.append("Durée adaptée pour débuter")
        
        # Safety level preference (prefer lower safety levels for beginners)
        if activity.safety_level <= 2:
            score += 15.0
            reasons.append("Niveau de sécurité adapté")
        elif activity.safety_level >= 4:
            score -= 10.0
            reasons.append("Niveau de sécurité élevé")
        
        # Seasonality bonus (prefer activities available in current season)
        # Note: This could be enhanced with actual date checking
        if not activity.seasonality or 'toutes' in activity.seasonality:
            score += 5.0
            reasons.append("Disponible toute l'année")
        
        # Student bonus for student-specific activities
        if user.is_student and activity.is_student_only:
            score += 20.0
            reasons.append("Activité réservée aux élèves MFR")
        
        # Availability matching
        if user.availability:
            # This is simplified - in reality, you'd match actual scheduling
            score += 5.0
            reasons.append("Compatible avec votre disponibilité")
        
        # Ensure minimum score
        score = max(score, 0.0)
        
        return score, reasons