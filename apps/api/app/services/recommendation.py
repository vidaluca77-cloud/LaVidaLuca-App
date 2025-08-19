import openai
from typing import List, Dict, Any
from sqlalchemy.orm import Session

from app.config import settings
from app.models.models import User, Activity, Participation
from app.schemas.recommendation import ActivityRecommendation

# Configure OpenAI
openai.api_key = settings.openai_api_key


class RecommendationService:
    """Service for AI-powered activity recommendations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_recommendations(
        self, 
        user: User, 
        limit: int = 5
    ) -> List[ActivityRecommendation]:
        """Get personalized activity recommendations for a user."""
        
        # Get user's completed activities to avoid recommending them again
        completed_activity_ids = [
            p.activity_id for p in user.participations 
            if p.status == "completed"
        ]
        
        # Get available activities
        available_activities = self.db.query(Activity).filter(
            Activity.is_active == True,
            ~Activity.id.in_(completed_activity_ids)
        ).all()
        
        if not available_activities:
            return []
        
        # Calculate recommendations using both rule-based and AI-enhanced scoring
        recommendations = []
        
        for activity in available_activities:
            score, reasons = self._calculate_activity_score(user, activity)
            
            # Enhanced scoring with AI if OpenAI key is available
            if settings.openai_api_key:
                ai_score, ai_reasons = self._get_ai_enhanced_score(user, activity)
                score = (score + ai_score) / 2
                reasons.extend(ai_reasons)
            
            recommendations.append(ActivityRecommendation(
                activity=activity,
                score=score,
                reasons=reasons,
                confidence=min(score / 100, 1.0)
            ))
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]
    
    def _calculate_activity_score(self, user: User, activity: Activity) -> tuple[float, List[str]]:
        """Calculate activity compatibility score using rule-based logic."""
        score = 0.0
        reasons = []
        
        # Skills matching
        user_skills = user.skills or []
        activity_skills = activity.skill_tags or []
        
        common_skills = set(user_skills) & set(activity_skills)
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Category preferences
        user_preferences = user.preferences or []
        if activity.category in user_preferences:
            score += 25
            category_names = {
                'agri': 'Agriculture',
                'transfo': 'Transformation',
                'artisanat': 'Artisanat',
                'nature': 'Environnement',
                'social': 'Animation'
            }
            reasons.append(f"Catégorie préférée : {category_names.get(activity.category, activity.category)}")
        
        # Duration matching (prefer shorter durations for beginners)
        user_completed_count = len([p for p in user.participations if p.status == "completed"])
        if user_completed_count < 3 and activity.duration_min <= 90:
            score += 10
            reasons.append("Durée adaptée pour débuter")
        elif user_completed_count >= 3 and activity.duration_min > 90:
            score += 5
            reasons.append("Durée adaptée à votre expérience")
        
        # Safety level (prefer lower safety levels for beginners)
        if user_completed_count < 5 and activity.safety_level <= 2:
            score += 10
            if activity.safety_level == 1:
                reasons.append("Activité sans risque particulier")
            else:
                reasons.append("Niveau de sécurité approprié")
        
        # Difficulty matching
        if user_completed_count < 3 and activity.difficulty_level <= 2:
            score += 8
            reasons.append("Niveau de difficulté adapté")
        elif user_completed_count >= 5 and activity.difficulty_level >= 3:
            score += 8
            reasons.append("Niveau de difficulté adapté à votre expérience")
        
        # Availability simulation (in real implementation, this would check calendar)
        user_availability = user.availability or []
        if user_availability:
            score += 15
            reasons.append("Compatible avec vos disponibilités")
        
        # Popularity boost (activities with good ratings)
        participations = self.db.query(Participation).filter(
            Participation.activity_id == activity.id,
            Participation.rating.isnot(None)
        ).all()
        
        if participations:
            avg_rating = sum(p.rating for p in participations) / len(participations)
            if avg_rating >= 4:
                score += 5
                reasons.append("Activité très bien notée")
        
        return score, reasons
    
    def _get_ai_enhanced_score(self, user: User, activity: Activity) -> tuple[float, List[str]]:
        """Get AI-enhanced scoring using OpenAI API."""
        try:
            # Prepare user profile for AI
            user_profile = {
                "skills": user.skills or [],
                "preferences": user.preferences or [],
                "completed_activities": len([p for p in user.participations if p.status == "completed"]),
                "location": user.location or "Non spécifié"
            }
            
            # Prepare activity info for AI
            activity_info = {
                "title": activity.title,
                "category": activity.category,
                "summary": activity.summary,
                "skills_required": activity.skill_tags or [],
                "duration": activity.duration_min,
                "difficulty": activity.difficulty_level,
                "safety_level": activity.safety_level
            }
            
            prompt = f"""
            En tant qu'expert en formation agricole et insertion sociale, analysez la compatibilité entre ce profil utilisateur et cette activité.
            
            Profil utilisateur:
            - Compétences: {user_profile['skills']}
            - Préférences: {user_profile['preferences']}
            - Activités complétées: {user_profile['completed_activities']}
            - Localisation: {user_profile['location']}
            
            Activité:
            - Titre: {activity_info['title']}
            - Catégorie: {activity_info['category']}
            - Résumé: {activity_info['summary']}
            - Compétences requises: {activity_info['skills_required']}
            - Durée: {activity_info['duration']} minutes
            - Difficulté: {activity_info['difficulty']}/5
            - Niveau sécurité: {activity_info['safety_level']}/3
            
            Donnez un score de 0 à 50 et 2-3 raisons spécifiques pourquoi cette activité conviendrait ou ne conviendrait pas à cet utilisateur.
            
            Réponse au format: SCORE:[nombre]|RAISONS:[raison1;raison2;raison3]
            """
            
            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            result = response.choices[0].text.strip()
            
            # Parse the response
            score_part, reasons_part = result.split("|")
            score = float(score_part.split(":")[1])
            reasons = reasons_part.split(":")[1].split(";")
            
            return score, [r.strip() for r in reasons if r.strip()]
            
        except Exception as e:
            # Fallback to basic scoring if AI fails
            print(f"AI scoring failed: {e}")
            return 0, ["Analyse IA indisponible"]
    
    def get_activity_recommendations_by_preferences(
        self,
        skills: List[str] = None,
        preferences: List[str] = None,
        availability: List[str] = None,
        limit: int = 5
    ) -> List[ActivityRecommendation]:
        """Get activity recommendations based on specific preferences (for anonymous users)."""
        
        available_activities = self.db.query(Activity).filter(Activity.is_active == True).all()
        
        recommendations = []
        
        for activity in available_activities:
            score = 0.0
            reasons = []
            
            # Skills matching
            if skills:
                common_skills = set(skills) & set(activity.skill_tags or [])
                if common_skills:
                    score += len(common_skills) * 15
                    reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
            
            # Category preferences
            if preferences and activity.category in preferences:
                score += 25
                category_names = {
                    'agri': 'Agriculture',
                    'transfo': 'Transformation', 
                    'artisanat': 'Artisanat',
                    'nature': 'Environnement',
                    'social': 'Animation'
                }
                reasons.append(f"Catégorie sélectionnée : {category_names.get(activity.category, activity.category)}")
            
            # Beginner-friendly scoring
            if activity.duration_min <= 90:
                score += 10
                reasons.append("Durée adaptée pour découvrir")
            
            if activity.safety_level <= 2:
                score += 10
                reasons.append("Activité sécurisée")
                
            if activity.difficulty_level <= 2:
                score += 8
                reasons.append("Accessible aux débutants")
            
            if score > 0:
                recommendations.append(ActivityRecommendation(
                    activity=activity,
                    score=score,
                    reasons=reasons,
                    confidence=min(score / 100, 1.0)
                ))
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x.score, reverse=True)
        return recommendations[:limit]