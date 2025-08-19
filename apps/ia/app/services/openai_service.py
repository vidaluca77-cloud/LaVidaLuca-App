"""
OpenAI service for AI-powered recommendations
"""

import openai
from typing import List, Dict, Any, Optional
import json
import logging
from app.core.config import settings
from app.schemas.schemas import UserProfileBase, Activity, ActivityCategory, DifficultyLevel

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service for OpenAI integration"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured")
    
    async def generate_recommendations(
        self,
        user_profile: UserProfileBase,
        available_activities: List[Activity],
        max_recommendations: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered activity recommendations for a user
        """
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI not configured, falling back to rule-based recommendations")
            return self._fallback_recommendations(user_profile, available_activities, max_recommendations)
        
        try:
            # Prepare prompt with user profile and activities
            prompt = self._create_recommendation_prompt(user_profile, available_activities)
            
            client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content
            recommendations = self._parse_ai_recommendations(ai_response, available_activities)
            
            return recommendations[:max_recommendations]
            
        except Exception as e:
            logger.error(f"OpenAI recommendation error: {str(e)}")
            return self._fallback_recommendations(user_profile, available_activities, max_recommendations)
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for the AI"""
        return """
        Tu es un expert en formation agricole et pédagogique pour le projet La Vida Luca.
        Ton rôle est de recommander des activités adaptées au profil de chaque utilisateur.
        
        La Vida Luca est un réseau de fermes pédagogiques qui forme des jeunes en MFR (Maison Familiale Rurale)
        aux métiers de l'agriculture durable, de l'artisanat et de l'environnement.
        
        Les activités sont organisées en 5 catégories :
        - agri : Agriculture (élevage, cultures, soins aux animaux)
        - transfo : Transformation (fromage, conserves, pain)
        - artisanat : Artisanat (menuiserie, construction, réparation)
        - nature : Environnement (plantation, compostage, écologie)
        - social : Animation (accueil, visites, ateliers enfants)
        
        Tes recommandations doivent être :
        1. Adaptées aux compétences et préférences de l'utilisateur
        2. Respectueuses de sa disponibilité et localisation
        3. Progressives dans la difficulté
        4. Éducatives et formatrices
        5. Sécurisées selon le niveau de l'utilisateur
        
        Réponds toujours en JSON avec le format :
        {
          "recommendations": [
            {
              "activity_id": 1,
              "score": 0.95,
              "reasons": ["raison 1", "raison 2"],
              "explanation": "Explication détaillée de pourquoi cette activité convient"
            }
          ]
        }
        """
    
    def _create_recommendation_prompt(
        self,
        user_profile: UserProfileBase,
        activities: List[Activity]
    ) -> str:
        """Create recommendation prompt"""
        
        # Format user profile
        profile_text = f"""
        Profil utilisateur :
        - Compétences : {', '.join(user_profile.skills) if user_profile.skills else 'Aucune'}
        - Disponibilités : {', '.join(user_profile.availability) if user_profile.availability else 'Non spécifiée'}
        - Localisation : {user_profile.location or 'Non spécifiée'}
        - Préférences : {', '.join(user_profile.preferences) if user_profile.preferences else 'Aucune'}
        - Niveau MFR : {user_profile.mfr_level or 'Non spécifié'}
        - Tranche d'âge : {user_profile.age_range or 'Non spécifiée'}
        - Bio : {user_profile.bio or 'Non renseignée'}
        """
        
        # Format activities
        activities_text = "Activités disponibles :\n"
        for activity in activities:
            activities_text += f"""
        - ID {activity.id}: {activity.title} ({activity.category})
          Résumé : {activity.summary}
          Durée : {activity.duration_min} min
          Compétences : {', '.join(activity.skill_tags)}
          Saisonnalité : {', '.join(activity.seasonality)}
          Niveau sécurité : {activity.safety_level}/5
          Niveau : {activity.difficulty_level}
          Matériel : {', '.join(activity.materials)}
        """
        
        return f"""
        {profile_text}
        
        {activities_text}
        
        Recommande au maximum 5 activités les plus adaptées à ce profil.
        Calcule un score de 0.0 à 1.0 pour chaque recommandation.
        Explique pourquoi chaque activité convient au profil.
        """
    
    def _parse_ai_recommendations(
        self,
        ai_response: str,
        activities: List[Activity]
    ) -> List[Dict[str, Any]]:
        """Parse AI response into structured recommendations"""
        try:
            # Extract JSON from response
            response_data = json.loads(ai_response)
            recommendations = response_data.get("recommendations", [])
            
            # Create activity ID to activity mapping
            activity_map = {activity.id: activity for activity in activities}
            
            parsed_recommendations = []
            for rec in recommendations:
                activity_id = rec.get("activity_id")
                if activity_id in activity_map:
                    parsed_recommendations.append({
                        "activity_id": activity_id,
                        "activity": activity_map[activity_id],
                        "score": float(rec.get("score", 0.5)),
                        "reasons": rec.get("reasons", []),
                        "ai_explanation": rec.get("explanation", "")
                    })
            
            return parsed_recommendations
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            return []
    
    def _fallback_recommendations(
        self,
        user_profile: UserProfileBase,
        activities: List[Activity],
        max_recommendations: int
    ) -> List[Dict[str, Any]]:
        """
        Fallback rule-based recommendations when OpenAI is not available
        """
        scored_activities = []
        
        for activity in activities:
            score = self._calculate_rule_based_score(user_profile, activity)
            if score > 0.3:  # Only recommend activities with decent match
                scored_activities.append({
                    "activity_id": activity.id,
                    "activity": activity,
                    "score": score,
                    "reasons": self._generate_rule_based_reasons(user_profile, activity),
                    "ai_explanation": f"Activité recommandée basée sur vos préférences pour {activity.category} et vos compétences."
                })
        
        # Sort by score and return top recommendations
        scored_activities.sort(key=lambda x: x["score"], reverse=True)
        return scored_activities[:max_recommendations]
    
    def _calculate_rule_based_score(
        self,
        user_profile: UserProfileBase,
        activity: Activity
    ) -> float:
        """Calculate rule-based matching score"""
        score = 0.0
        
        # Category preference match
        if user_profile.preferences and activity.category in user_profile.preferences:
            score += 0.3
        
        # Skill match
        if user_profile.skills:
            matching_skills = set(user_profile.skills) & set(activity.skill_tags)
            if matching_skills:
                score += 0.3 * (len(matching_skills) / max(len(activity.skill_tags), 1))
        
        # Difficulty level match
        if user_profile.mfr_level:
            if user_profile.mfr_level == activity.difficulty_level:
                score += 0.2
            elif user_profile.mfr_level == "beginner" and activity.difficulty_level == "intermediate":
                score += 0.1
        
        # Safety level consideration
        if activity.safety_level <= 2:  # Safer activities get slight boost
            score += 0.1
        
        # Base interest score
        score += 0.1
        
        return min(score, 1.0)
    
    def _generate_rule_based_reasons(
        self,
        user_profile: UserProfileBase,
        activity: Activity
    ) -> List[str]:
        """Generate reasons for rule-based recommendations"""
        reasons = []
        
        if user_profile.preferences and activity.category in user_profile.preferences:
            reasons.append(f"Correspond à votre intérêt pour {activity.category}")
        
        if user_profile.skills:
            matching_skills = set(user_profile.skills) & set(activity.skill_tags)
            if matching_skills:
                reasons.append(f"Utilise vos compétences : {', '.join(matching_skills)}")
        
        if user_profile.mfr_level == activity.difficulty_level:
            reasons.append(f"Adapté à votre niveau {user_profile.mfr_level}")
        
        if activity.safety_level <= 2:
            reasons.append("Activité sécurisée pour débuter")
        
        if not reasons:
            reasons.append("Activité formative recommandée")
        
        return reasons


# Global service instance
openai_service = OpenAIService()