"""
OpenAI integration service.
"""
import json
from typing import List, Dict, Any, Optional
import openai
from openai import OpenAI

from ..core.config import settings
from ..models.user import User
from ..models.activity import Activity
from ..schemas.activity import ActivitySuggestion

# Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)


class OpenAIService:
    """OpenAI integration service for activity suggestions and content analysis."""
    
    def __init__(self):
        self.client = client
    
    async def generate_activity_suggestions(
        self,
        user: User,
        available_activities: List[Activity],
        limit: int = 5
    ) -> List[ActivitySuggestion]:
        """Generate personalized activity suggestions for a user."""
        
        # Prepare user profile for AI
        user_profile = self._prepare_user_profile(user)
        
        # Prepare activities context
        activities_context = self._prepare_activities_context(available_activities)
        
        # Create prompt
        prompt = self._create_suggestion_prompt(user_profile, activities_context, limit)
        
        try:
            response = await self._call_openai_completion(prompt)
            suggestions = self._parse_suggestions_response(response, available_activities)
            return suggestions[:limit]
        
        except Exception as e:
            # Fallback to simple scoring if AI fails
            return self._fallback_suggestions(user, available_activities, limit)
    
    async def analyze_user_profile(self, user: User) -> Dict[str, Any]:
        """Analyze user profile and provide insights."""
        
        user_data = {
            "bio": user.bio or "",
            "skills": user.profile_data.get("skills", []) if user.profile_data else [],
            "preferences": user.profile_data.get("preferences", {}) if user.profile_data else {},
            "location": user.location or ""
        }
        
        prompt = f"""
        Analyze this user profile and provide insights about their interests, learning style, and recommendations:
        
        User Profile:
        - Bio: {user_data['bio']}
        - Skills: {', '.join(user_data['skills'])}
        - Location: {user_data['location']}
        - Preferences: {json.dumps(user_data['preferences'])}
        
        Please provide:
        1. Key interests and strengths
        2. Learning style preferences
        3. Recommended activity categories
        4. Skill development opportunities
        
        Respond in JSON format with keys: interests, learning_style, recommended_categories, skill_opportunities
        """
        
        try:
            response = await self._call_openai_completion(prompt)
            return json.loads(response)
        except Exception:
            return {
                "interests": ["agriculture", "sustainability"],
                "learning_style": "practical",
                "recommended_categories": ["agri", "nature"],
                "skill_opportunities": ["gardening", "ecology"]
            }
    
    async def moderate_content(self, content: str) -> Dict[str, Any]:
        """Moderate content for inappropriate material."""
        
        try:
            response = self.client.moderations.create(input=content)
            result = response.results[0]
            
            return {
                "flagged": result.flagged,
                "categories": dict(result.categories),
                "category_scores": dict(result.category_scores)
            }
        
        except Exception:
            # Fallback - allow content if moderation fails
            return {
                "flagged": False,
                "categories": {},
                "category_scores": {}
            }
    
    async def enhance_activity_description(self, activity: Activity) -> str:
        """Generate enhanced description for an activity."""
        
        prompt = f"""
        Enhance this activity description for students in rural agricultural education:
        
        Title: {activity.title}
        Category: {activity.category}
        Current Summary: {activity.summary}
        Duration: {activity.duration_min} minutes
        Skills: {', '.join(activity.skill_tags or [])}
        
        Create an engaging, educational description that:
        1. Explains the learning objectives clearly
        2. Connects to real-world applications
        3. Highlights practical skills gained
        4. Uses encouraging, accessible language
        
        Keep it under 300 words and suitable for young learners.
        """
        
        try:
            response = await self._call_openai_completion(prompt)
            return response.strip()
        except Exception:
            return activity.description or activity.summary
    
    def _prepare_user_profile(self, user: User) -> Dict[str, Any]:
        """Prepare user profile data for AI processing."""
        return {
            "role": user.role,
            "skills": user.profile_data.get("skills", []) if user.profile_data else [],
            "interests": user.profile_data.get("preferences", {}).get("interests", []) if user.profile_data else [],
            "location": user.location or "",
            "experience_level": user.profile_data.get("experience_level", "beginner") if user.profile_data else "beginner"
        }
    
    def _prepare_activities_context(self, activities: List[Activity]) -> List[Dict[str, Any]]:
        """Prepare activities data for AI processing."""
        return [
            {
                "id": str(activity.id),
                "title": activity.title,
                "category": activity.category,
                "summary": activity.summary,
                "difficulty": activity.difficulty_level,
                "duration": activity.duration_min,
                "skills": activity.skill_tags or []
            }
            for activity in activities
        ]
    
    def _create_suggestion_prompt(
        self,
        user_profile: Dict[str, Any],
        activities: List[Dict[str, Any]],
        limit: int
    ) -> str:
        """Create prompt for activity suggestions."""
        return f"""
        You are an educational advisor for rural agricultural students. 
        
        User Profile:
        - Role: {user_profile['role']}
        - Skills: {', '.join(user_profile['skills'])}
        - Interests: {', '.join(user_profile['interests'])}
        - Experience: {user_profile['experience_level']}
        - Location: {user_profile['location']}
        
        Available Activities:
        {json.dumps(activities, indent=2)}
        
        Select the top {limit} most relevant activities for this user and explain why.
        
        Respond in JSON format:
        {{
            "suggestions": [
                {{
                    "activity_id": "uuid",
                    "score": 0.95,
                    "reasons": ["reason1", "reason2"]
                }}
            ]
        }}
        
        Consider: skill alignment, difficulty progression, interests, practical relevance.
        """
    
    async def _call_openai_completion(self, prompt: str) -> str:
        """Call OpenAI completion API."""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful educational advisor for rural agricultural education."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _parse_suggestions_response(
        self,
        response: str,
        activities: List[Activity]
    ) -> List[ActivitySuggestion]:
        """Parse AI response into ActivitySuggestion objects."""
        try:
            data = json.loads(response)
            suggestions = []
            
            activity_map = {str(activity.id): activity for activity in activities}
            
            for suggestion in data.get("suggestions", []):
                activity_id = suggestion.get("activity_id")
                if activity_id in activity_map:
                    suggestions.append(ActivitySuggestion(
                        activity=activity_map[activity_id],
                        score=suggestion.get("score", 0.5),
                        reasons=suggestion.get("reasons", [])
                    ))
            
            return suggestions
        
        except Exception:
            return []
    
    def _fallback_suggestions(
        self,
        user: User,
        activities: List[Activity],
        limit: int
    ) -> List[ActivitySuggestion]:
        """Fallback activity suggestions when AI is unavailable."""
        suggestions = []
        user_skills = user.profile_data.get("skills", []) if user.profile_data else []
        
        for activity in activities[:limit]:
            # Simple scoring based on skill overlap
            skill_overlap = len(set(user_skills) & set(activity.skill_tags or []))
            score = min(0.8, 0.3 + (skill_overlap * 0.1))
            
            reasons = ["Matches your experience level"]
            if skill_overlap > 0:
                reasons.append(f"Uses {skill_overlap} of your existing skills")
            
            suggestions.append(ActivitySuggestion(
                activity=activity,
                score=score,
                reasons=reasons
            ))
        
        return sorted(suggestions, key=lambda x: x.score, reverse=True)[:limit]