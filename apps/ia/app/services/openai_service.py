"""
OpenAI service for activity recommendations
"""
import json
from typing import List, Dict, Any
from openai import OpenAI
from ..core.config import settings
from ..schemas.schemas import UserProfileBase, Activity


class OpenAIService:
    """Service for generating AI-powered activity recommendations."""
    
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
    
    async def generate_recommendations_explanation(
        self, 
        user_profile: UserProfileBase, 
        activities: List[Activity],
        scores: Dict[int, int]
    ) -> Dict[int, str]:
        """
        Generate AI explanations for activity recommendations.
        
        Args:
            user_profile: User's profile data
            activities: List of recommended activities
            scores: Mapping of activity_id to score
            
        Returns:
            Dict mapping activity_id to AI explanation
        """
        if not self.client:
            return {}
        
        try:
            # Prepare context for AI
            profile_context = self._format_profile_context(user_profile)
            activities_context = self._format_activities_context(activities, scores)
            
            prompt = f"""
            En tant qu'expert en pédagogie agricole et insertion sociale pour La Vida Luca, 
            génère des explications personnalisées pour chaque recommandation d'activité.
            
            Profil utilisateur:
            {profile_context}
            
            Activités recommandées:
            {activities_context}
            
            Pour chaque activité, fournis une explication courte (2-3 phrases) expliquant pourquoi 
            cette activité correspond au profil. Concentre-toi sur:
            - Les compétences correspondantes
            - L'expérience pédagogique
            - L'insertion sociale
            - La progression dans l'apprentissage
            
            Réponds en JSON avec le format:
            {{"activity_id": "explication personnalisée", ...}}
            """
            
            response = await self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un expert en pédagogie agricole et insertion sociale."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            explanations = json.loads(content)
            
            # Convert string keys to int for activity IDs
            return {int(k): v for k, v in explanations.items()}
            
        except Exception as e:
            print(f"Error generating AI explanations: {e}")
            return {}
    
    def _format_profile_context(self, profile: UserProfileBase) -> str:
        """Format user profile for AI context."""
        return f"""
        - Compétences: {', '.join(profile.skills) if profile.skills else 'Non spécifiées'}
        - Préférences: {', '.join(profile.preferences) if profile.preferences else 'Non spécifiées'}
        - Disponibilités: {', '.join(profile.availability) if profile.availability else 'Non spécifiées'}
        - Niveau d'expérience: {profile.experience_level}
        - Localisation: {profile.location or 'Non spécifiée'}
        """
    
    def _format_activities_context(self, activities: List[Activity], scores: Dict[int, int]) -> str:
        """Format activities for AI context."""
        context = []
        for activity in activities:
            score = scores.get(activity.id, 0)
            context.append(f"""
            ID: {activity.id}
            Titre: {activity.title}
            Catégorie: {activity.category}
            Résumé: {activity.summary}
            Compétences requises: {', '.join(activity.skill_tags)}
            Durée: {activity.duration_min} minutes
            Score de correspondance: {score}/100
            """)
        return '\n'.join(context)


openai_service = OpenAIService()