"""
OpenAI integration for AI-powered activity recommendations
"""
import json
from typing import List, Dict, Any
from openai import OpenAI
from app.core.config import settings
from app.schemas.schemas import Activity, ActivitySuggestion
from app.models.models import User

class AIRecommendationService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if OpenAI service is available"""
        return self.client is not None
    
    async def generate_recommendations(
        self,
        user_profile: Dict[str, Any],
        activities: List[Activity],
        limit: int = 10
    ) -> List[ActivitySuggestion]:
        """
        Generate AI-powered activity recommendations based on user profile
        """
        if not self.is_available():
            return self._fallback_recommendations(user_profile, activities, limit)
        
        try:
            # Prepare context for OpenAI
            context = self._prepare_context(user_profile, activities)
            
            # Make OpenAI API call
            response = await self._call_openai(context, limit)
            
            # Parse response and create suggestions
            suggestions = self._parse_openai_response(response, activities)
            
            return suggestions[:limit]
        
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return self._fallback_recommendations(user_profile, activities, limit)
    
    def _prepare_context(self, user_profile: Dict[str, Any], activities: List[Activity]) -> str:
        """Prepare context string for OpenAI"""
        activities_json = []
        for activity in activities:
            activities_json.append({
                "id": activity.id,
                "title": activity.title,
                "category": activity.category,
                "summary": activity.summary,
                "skill_tags": activity.skill_tags,
                "seasonality": activity.seasonality,
                "safety_level": activity.safety_level,
                "duration_min": activity.duration_min
            })
        
        context = f"""
Voici le profil d'un utilisateur de La Vida Luca (formation agricole pour jeunes en MFR):

Profil utilisateur:
- Compétences: {user_profile.get('skills', [])}
- Disponibilités: {user_profile.get('availability', [])}
- Préférences de catégories: {user_profile.get('preferences', [])}
- Localisation: {user_profile.get('location', 'Non spécifiée')}

Activités disponibles:
{json.dumps(activities_json, indent=2, ensure_ascii=False)}

Consigne: Recommande les activités les plus pertinentes pour cet utilisateur en tenant compte de:
1. Ses compétences existantes
2. Ses disponibilités
3. Ses préférences de catégories
4. Le niveau de sécurité adapté
5. La progression pédagogique naturelle

Réponds uniquement avec un JSON contenant une liste d'objets avec:
- "activity_id": int
- "score": float (0-100)
- "reasons": array de strings expliquant pourquoi cette activité est recommandée

Exemple de format de réponse:
{{"recommendations": [{{"activity_id": 1, "score": 85.5, "reasons": ["Compétences correspondantes: elevage", "Adapté aux débutants"]}}]}}
"""
        return context
    
    async def _call_openai(self, context: str, limit: int) -> str:
        """Make actual OpenAI API call"""
        response = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en formation agricole et pédagogie pour les jeunes en MFR (Maisons Familiales Rurales). Tu recommandes des activités adaptées en fonction du profil des apprenants."
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            max_tokens=1500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
    
    def _parse_openai_response(self, response: str, activities: List[Activity]) -> List[ActivitySuggestion]:
        """Parse OpenAI response and create ActivitySuggestion objects"""
        suggestions = []
        activities_by_id = {activity.id: activity for activity in activities}
        
        try:
            # Parse JSON response
            response_data = json.loads(response)
            recommendations = response_data.get("recommendations", [])
            
            for rec in recommendations:
                activity_id = rec.get("activity_id")
                if activity_id in activities_by_id:
                    suggestion = ActivitySuggestion(
                        activity=activities_by_id[activity_id],
                        score=rec.get("score", 0.0),
                        reasons=rec.get("reasons", [])
                    )
                    suggestions.append(suggestion)
        
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing OpenAI response: {e}")
            # Return empty list if parsing fails
            return []
        
        return suggestions
    
    def _fallback_recommendations(
        self,
        user_profile: Dict[str, Any],
        activities: List[Activity],
        limit: int
    ) -> List[ActivitySuggestion]:
        """
        Fallback recommendation algorithm when OpenAI is not available
        """
        suggestions = []
        
        for activity in activities:
            score = 0
            reasons = []
            
            # Check skill matches
            common_skills = set(activity.skill_tags) & set(user_profile.get('skills', []))
            if common_skills:
                score += len(common_skills) * 15
                reasons.append(f"Compétences correspondantes: {', '.join(common_skills)}")
            
            # Check category preferences
            if activity.category in user_profile.get('preferences', []):
                score += 25
                reasons.append(f"Catégorie préférée: {activity.category}")
            
            # Prefer lower safety levels for beginners
            if len(user_profile.get('skills', [])) < 3 and activity.safety_level <= 1:
                score += 10
                reasons.append("Niveau de sécurité adapté aux débutants")
            
            # Prefer shorter activities for beginners
            if len(user_profile.get('skills', [])) < 3 and activity.duration_min <= 90:
                score += 5
                reasons.append("Durée adaptée pour débuter")
            
            if score > 0:
                suggestion = ActivitySuggestion(
                    activity=activity,
                    score=score,
                    reasons=reasons
                )
                suggestions.append(suggestion)
        
        # Sort by score and return top results
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:limit]

# Global instance
ai_service = AIRecommendationService()