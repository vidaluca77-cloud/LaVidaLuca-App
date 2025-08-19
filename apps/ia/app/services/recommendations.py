import json
from typing import List, Dict, Any
import openai
from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.user import UserProfile
from app.schemas.activity import Activity, ActivitySuggestion

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class RecommendationService:
    """Service for generating AI-powered activity recommendations"""
    
    @staticmethod
    async def generate_recommendations(
        user_profile: UserProfile,
        activities: List[Activity],
        max_recommendations: int = 5
    ) -> List[ActivitySuggestion]:
        """Generate personalized activity recommendations using OpenAI"""
        
        if not settings.OPENAI_API_KEY:
            # Fallback to simple matching when OpenAI is not configured
            return RecommendationService._simple_matching(user_profile, activities, max_recommendations)
        
        try:
            # Prepare context for OpenAI
            user_context = {
                "skills": user_profile.skills,
                "availability": user_profile.availability,
                "location": user_profile.location,
                "preferences": user_profile.preferences
            }
            
            activities_context = [
                {
                    "id": activity.id,
                    "title": activity.title,
                    "category": activity.category,
                    "summary": activity.summary,
                    "duration_min": activity.duration_min,
                    "skill_tags": activity.skill_tags,
                    "seasonality": activity.seasonality,
                    "safety_level": activity.safety_level,
                    "materials": activity.materials
                }
                for activity in activities
            ]
            
            prompt = f"""
            Tu es un conseiller pédagogique spécialisé dans les activités agricoles et artisanales pour les élèves de MFR (Maison Familiale Rurale).
            
            Profil de l'utilisateur:
            {json.dumps(user_context, indent=2, ensure_ascii=False)}
            
            Activités disponibles:
            {json.dumps(activities_context, indent=2, ensure_ascii=False)}
            
            Ta mission: recommander les {max_recommendations} meilleures activités pour cet utilisateur.
            
            Critères d'évaluation:
            1. Correspondance avec les compétences existantes ou à développer
            2. Adéquation avec les disponibilités
            3. Alignement avec les préférences de catégories
            4. Progression pédagogique (du simple au complexe)
            5. Diversité des apprentissages
            
            Réponds uniquement avec un JSON valide contenant un array de recommendations:
            [
                {{
                    "activity_id": <id>,
                    "score": <0.0-1.0>,
                    "reasons": ["raison 1", "raison 2", "raison 3"]
                }}
            ]
            """
            
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Tu es un expert en pédagogie agricole et artisanale."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            # Parse OpenAI response
            content = response.choices[0].message.content.strip()
            recommendations_data = json.loads(content)
            
            # Convert to ActivitySuggestion objects
            suggestions = []
            activities_dict = {activity.id: activity for activity in activities}
            
            for rec in recommendations_data[:max_recommendations]:
                activity_id = rec.get("activity_id")
                if activity_id in activities_dict:
                    suggestion = ActivitySuggestion(
                        activity=activities_dict[activity_id],
                        score=rec.get("score", 0.5),
                        reasons=rec.get("reasons", [])
                    )
                    suggestions.append(suggestion)
            
            return suggestions
            
        except Exception as e:
            print(f"OpenAI recommendation error: {e}")
            # Fallback to simple matching
            return RecommendationService._simple_matching(user_profile, activities, max_recommendations)
    
    @staticmethod
    def _simple_matching(
        user_profile: UserProfile,
        activities: List[Activity],
        max_recommendations: int
    ) -> List[ActivitySuggestion]:
        """Simple fallback recommendation algorithm"""
        
        suggestions = []
        
        for activity in activities:
            score = 0.0
            reasons = []
            
            # Score based on skill matching
            skill_matches = set(user_profile.skills) & set(activity.skill_tags)
            if skill_matches:
                score += 0.4
                reasons.append(f"Correspond à vos compétences: {', '.join(skill_matches)}")
            
            # Score based on category preferences
            if activity.category.value in user_profile.preferences:
                score += 0.3
                reasons.append(f"Catégorie préférée: {activity.category.value}")
            
            # Score based on duration and availability
            if "weekend" in user_profile.availability and activity.duration_min <= 120:
                score += 0.2
                reasons.append("Durée adaptée au weekend")
            elif "semaine" in user_profile.availability:
                score += 0.2
                reasons.append("Disponible en semaine")
            
            # Bonus for featured activities
            if getattr(activity, 'is_featured', False):
                score += 0.1
                reasons.append("Activité mise en avant")
            
            if score > 0:
                suggestions.append(ActivitySuggestion(
                    activity=activity,
                    score=min(score, 1.0),
                    reasons=reasons
                ))
        
        # Sort by score and return top recommendations
        suggestions.sort(key=lambda x: x.score, reverse=True)
        return suggestions[:max_recommendations]