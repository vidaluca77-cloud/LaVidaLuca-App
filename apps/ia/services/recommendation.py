import openai
from typing import List, Dict, Any
from config import settings
from schemas.activity import Activity
from schemas.user import UserProfile
from schemas.recommendation import Suggestion
import json

openai.api_key = settings.openai_api_key


class RecommendationService:
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    def calculate_basic_matching(self, user_profile: UserProfile, activities: List[Activity]) -> List[Suggestion]:
        """
        Basic recommendation algorithm without AI
        """
        suggestions = []
        
        for activity in activities:
            score = 0.0
            reasons = []
            
            # Skill matching
            matching_skills = set(user_profile.skills) & set(activity.skill_tags)
            if matching_skills:
                skill_score = len(matching_skills) / len(activity.skill_tags) if activity.skill_tags else 0
                score += skill_score * 0.4
                reasons.append(f"Compétences correspondantes: {', '.join(matching_skills)}")
            
            # Category preference matching
            if activity.category in user_profile.preferences:
                score += 0.3
                reasons.append(f"Catégorie préférée: {activity.category}")
            
            # Safety level matching (lower is easier)
            if activity.safety_level <= 2:
                score += 0.2
                reasons.append("Niveau de sécurité adapté")
            
            # Duration preference (shorter activities are generally preferred)
            if activity.duration_min and activity.duration_min <= 90:
                score += 0.1
                reasons.append("Durée adaptée")
            
            if score > 0:
                suggestions.append(Suggestion(
                    activity=activity,
                    score=score,
                    reasons=reasons
                ))
        
        # Sort by score descending
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions
    
    async def get_ai_recommendations(self, user_profile: UserProfile, activities: List[Activity], limit: int = 5) -> List[Suggestion]:
        """
        Get AI-powered recommendations using OpenAI
        """
        try:
            # Prepare activity data for AI
            activity_data = []
            for activity in activities:
                activity_data.append({
                    "id": activity.id,
                    "title": activity.title,
                    "category": activity.category,
                    "summary": activity.summary,
                    "skill_tags": activity.skill_tags,
                    "duration_min": activity.duration_min,
                    "safety_level": activity.safety_level,
                    "seasonality": activity.seasonality
                })
            
            prompt = f"""
            Analyse ce profil utilisateur et recommande les {limit} meilleures activités pour cette personne.
            
            Profil utilisateur:
            - Compétences: {user_profile.skills}
            - Disponibilité: {user_profile.availability}
            - Localisation: {user_profile.location}
            - Préférences: {user_profile.preferences}
            
            Activités disponibles:
            {json.dumps(activity_data, indent=2, ensure_ascii=False)}
            
            Réponds avec un JSON contenant un array de recommendations avec cette structure:
            {{
                "recommendations": [
                    {{
                        "activity_id": int,
                        "score": float (entre 0 et 1),
                        "reasons": ["raison 1", "raison 2", ...]
                    }}
                ]
            }}
            
            Base tes recommandations sur:
            1. La correspondance entre les compétences de l'utilisateur et les skill_tags de l'activité
            2. Les préférences de catégorie
            3. Le niveau de sécurité approprié
            4. La disponibilité et la durée
            5. La saisonnalité si pertinente
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un expert en recommandations d'activités agricoles et artisanales pour les jeunes en formation. Réponds uniquement en JSON valide."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            recommendations_data = json.loads(ai_response)
            
            # Convert AI recommendations to Suggestion objects
            suggestions = []
            activities_dict = {activity.id: activity for activity in activities}
            
            for rec in recommendations_data.get("recommendations", []):
                activity_id = rec.get("activity_id")
                if activity_id in activities_dict:
                    suggestions.append(Suggestion(
                        activity=activities_dict[activity_id],
                        score=rec.get("score", 0.0),
                        reasons=rec.get("reasons", [])
                    ))
            
            return suggestions[:limit]
            
        except Exception as e:
            print(f"AI recommendation error: {e}")
            # Fallback to basic matching if AI fails
            basic_suggestions = self.calculate_basic_matching(user_profile, activities)
            return basic_suggestions[:limit]


recommendation_service = RecommendationService()