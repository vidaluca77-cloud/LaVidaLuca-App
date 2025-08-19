"""
AI-powered matching service for La Vida Luca using OpenAI.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..core.config import settings
from ..models import User, Activity, ActivitySuggestion
from ..schemas.activity import ActivitySuggestionCreate

logger = logging.getLogger(__name__)


class MatchingService:
    """AI-powered activity matching service."""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            logger.warning("OpenAI API key not configured - AI features will be disabled")
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_activity_suggestions(
        self, 
        user: User, 
        db: AsyncSession,
        limit: int = 5
    ) -> List[ActivitySuggestion]:
        """Generate personalized activity suggestions for a user."""
        if not self.client:
            logger.warning("OpenAI client not available - returning empty suggestions")
            return []
        
        try:
            # Get user profile and preferences
            user_profile = self._build_user_profile(user)
            
            # Get available activities
            activities = await self._get_available_activities(db)
            
            if not activities:
                logger.info("No activities available for suggestions")
                return []
            
            # Generate AI suggestions
            suggestions = await self._get_ai_suggestions(user_profile, activities, limit)
            
            # Create suggestion records in database
            suggestion_records = []
            for suggestion in suggestions:
                activity_id = suggestion.get('activity_id')
                if activity_id:
                    # Check if suggestion already exists
                    existing = await db.execute(
                        select(ActivitySuggestion).where(
                            and_(
                                ActivitySuggestion.user_id == user.id,
                                ActivitySuggestion.activity_id == activity_id
                            )
                        )
                    )
                    if not existing.scalar_one_or_none():
                        suggestion_record = ActivitySuggestion(
                            user_id=user.id,
                            activity_id=activity_id,
                            suggestion_reason=suggestion.get('reason'),
                            confidence_score=suggestion.get('confidence', 0.5),
                            ai_generated=True,
                            user_context=json.dumps(user_profile),
                            matching_criteria=json.dumps(suggestion.get('criteria', {}))
                        )
                        db.add(suggestion_record)
                        suggestion_records.append(suggestion_record)
            
            await db.commit()
            
            # Refresh objects to get full data
            for record in suggestion_records:
                await db.refresh(record)
            
            return suggestion_records
            
        except Exception as e:
            logger.error(f"Error generating activity suggestions: {e}")
            await db.rollback()
            return []
    
    def _build_user_profile(self, user: User) -> Dict[str, Any]:
        """Build a comprehensive user profile for AI matching."""
        profile = {
            "role": user.role,
            "institution": user.institution,
            "location": user.location,
            "expertise_areas": json.loads(user.expertise_areas) if user.expertise_areas else [],
            "interests": json.loads(user.interests) if user.interests else [],
            "bio": user.bio,
            "experience_level": self._infer_experience_level(user)
        }
        return profile
    
    def _infer_experience_level(self, user: User) -> str:
        """Infer user experience level based on role and other factors."""
        if user.role == "teacher":
            return "advanced"
        elif user.role == "coordinator":
            return "expert"
        elif user.role == "admin":
            return "expert"
        else:
            return "beginner"
    
    async def _get_available_activities(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """Get available published activities for matching."""
        result = await db.execute(
            select(Activity).where(
                and_(
                    Activity.is_published == True,
                    Activity.approval_status == "approved"
                )
            ).limit(50)  # Limit for AI processing
        )
        activities = result.scalars().all()
        
        return [
            {
                "id": activity.id,
                "title": activity.title,
                "description": activity.description,
                "category": activity.category,
                "subcategory": activity.subcategory,
                "difficulty_level": activity.difficulty_level,
                "duration_minutes": activity.duration_minutes,
                "location_type": activity.location_type,
                "tags": json.loads(activity.tags) if activity.tags else [],
                "learning_objectives": json.loads(activity.learning_objectives) if activity.learning_objectives else [],
                "competencies_developed": json.loads(activity.competencies_developed) if activity.competencies_developed else [],
                "sustainability_score": activity.sustainability_score,
                "equipment_needed": json.loads(activity.equipment_needed) if activity.equipment_needed else []
            }
            for activity in activities
        ]
    
    async def _get_ai_suggestions(
        self, 
        user_profile: Dict[str, Any], 
        activities: List[Dict[str, Any]], 
        limit: int
    ) -> List[Dict[str, Any]]:
        """Get AI-powered activity suggestions using OpenAI."""
        try:
            prompt = self._build_matching_prompt(user_profile, activities, limit)
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an educational activity recommendation system for MFR (Maisons Familiales Rurales) - agricultural and rural training institutions. Your goal is to match students and teachers with appropriate learning activities based on their profiles, interests, and educational needs.

Consider factors like:
- User's role and experience level
- Educational objectives alignment
- Difficulty appropriateness
- Interest and expertise matching
- Practical applicability
- Sustainability and agricultural focus

Respond with a JSON array of recommendations, each containing:
- activity_id: string
- reason: detailed explanation (in French)
- confidence: float between 0.0 and 1.0
- criteria: object with matching criteria used"""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            suggestions = json.loads(content)
            
            return suggestions[:limit]
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            return []
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return []
    
    def _build_matching_prompt(
        self, 
        user_profile: Dict[str, Any], 
        activities: List[Dict[str, Any]], 
        limit: int
    ) -> str:
        """Build the prompt for AI matching."""
        prompt = f"""
Profil utilisateur:
- Rôle: {user_profile.get('role', 'student')}
- Niveau d'expérience: {user_profile.get('experience_level', 'beginner')}
- Institution: {user_profile.get('institution', 'Non spécifiée')}
- Localisation: {user_profile.get('location', 'Non spécifiée')}
- Domaines d'expertise: {', '.join(user_profile.get('expertise_areas', []))}
- Intérêts: {', '.join(user_profile.get('interests', []))}

Activités disponibles:
{json.dumps(activities, indent=2, ensure_ascii=False)}

Recommandez les {limit} meilleures activités pour cet utilisateur. Expliquez en français pourquoi chaque activité convient à ce profil.
"""
        return prompt
    
    async def find_similar_activities(
        self, 
        activity: Activity, 
        db: AsyncSession, 
        limit: int = 5
    ) -> List[Activity]:
        """Find activities similar to the given activity."""
        # Simple similarity based on category, tags, and difficulty for now
        # Could be enhanced with embeddings in the future
        
        result = await db.execute(
            select(Activity).where(
                and_(
                    Activity.id != activity.id,
                    Activity.is_published == True,
                    Activity.approval_status == "approved",
                    Activity.category == activity.category
                )
            ).limit(limit)
        )
        
        return result.scalars().all()
    
    async def get_user_recommendations(
        self, 
        user_id: str, 
        db: AsyncSession,
        include_viewed: bool = False
    ) -> List[ActivitySuggestion]:
        """Get existing recommendations for a user."""
        query = select(ActivitySuggestion).where(ActivitySuggestion.user_id == user_id)
        
        if not include_viewed:
            query = query.where(ActivitySuggestion.is_viewed == False)
        
        result = await db.execute(query.order_by(ActivitySuggestion.created_at.desc()))
        return result.scalars().all()
    
    async def mark_suggestion_viewed(
        self, 
        suggestion_id: str, 
        db: AsyncSession
    ) -> bool:
        """Mark a suggestion as viewed."""
        try:
            result = await db.execute(
                select(ActivitySuggestion).where(ActivitySuggestion.id == suggestion_id)
            )
            suggestion = result.scalar_one_or_none()
            
            if suggestion:
                suggestion.is_viewed = True
                suggestion.viewed_at = func.now()
                await db.commit()
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error marking suggestion as viewed: {e}")
            await db.rollback()
            return False