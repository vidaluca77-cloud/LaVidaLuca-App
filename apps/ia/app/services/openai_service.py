"""
OpenAI service for AI-powered recommendations.
"""
import json
from typing import List, Dict, Optional
import openai
from sqlalchemy.orm import Session

from ..core.config import settings
from ..models.activity import Activity
from ..models.user import User
from ..schemas.recommendation import RecommendationRequest


class OpenAIService:
    """Service for interacting with OpenAI API."""
    
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        else:
            openai.api_key = None
    
    async def generate_activity_recommendations(
        self,
        user: User,
        activities: List[Activity],
        request: RecommendationRequest,
        db: Session
    ) -> List[Dict]:
        """
        Generate AI-powered activity recommendations for a user.
        """
        if not openai.api_key:
            # Fallback to rule-based recommendations if no OpenAI key
            return self._rule_based_recommendations(user, activities, request)
        
        try:
            # Prepare user context
            user_context = self._prepare_user_context(user, request)
            
            # Prepare activities context
            activities_context = self._prepare_activities_context(activities)
            
            # Create prompt for OpenAI
            prompt = self._create_recommendation_prompt(user_context, activities_context)
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant specializing in agricultural and educational activity recommendations for MFR (Maison Familiale Rurale) students. Provide personalized recommendations based on user preferences, learning objectives, and practical constraints."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse response
            recommendations = self._parse_openai_response(response.choices[0].message.content, activities)
            return recommendations
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based recommendations
            return self._rule_based_recommendations(user, activities, request)
    
    def _prepare_user_context(self, user: User, request: RecommendationRequest) -> str:
        """Prepare user context for the AI prompt."""
        context = f"User: {user.full_name or user.username}\n"
        context += f"Bio: {user.bio or 'No bio provided'}\n"
        
        if request.user_interests:
            context += f"Interests: {', '.join(request.user_interests)}\n"
        
        if request.preferred_difficulty:
            context += f"Preferred difficulty level: {request.preferred_difficulty}/5\n"
        
        if request.max_duration:
            context += f"Maximum duration: {request.max_duration} hours\n"
        
        if request.location_preference:
            context += f"Location preference: {request.location_preference}\n"
        
        return context
    
    def _prepare_activities_context(self, activities: List[Activity]) -> str:
        """Prepare activities context for the AI prompt."""
        context = "Available activities:\n"
        for i, activity in enumerate(activities, 1):
            context += f"{i}. {activity.title}\n"
            context += f"   Category: {activity.category}\n"
            context += f"   Difficulty: {activity.difficulty_level}/5\n"
            context += f"   Duration: {activity.duration_hours or 'Not specified'} hours\n"
            context += f"   Description: {activity.description[:200]}...\n"
            context += f"   Learning objectives: {activity.learning_objectives or 'Not specified'}\n\n"
        
        return context
    
    def _create_recommendation_prompt(self, user_context: str, activities_context: str) -> str:
        """Create the prompt for OpenAI recommendation."""
        prompt = f"""
Based on the following user profile and available activities, recommend the top 5 most suitable activities for this user.

{user_context}

{activities_context}

Please provide recommendations in the following JSON format:
[
    {{
        "activity_id": <activity_number>,
        "confidence_score": <0.0-1.0>,
        "reasoning": "<explanation why this activity suits the user>",
        "recommendation_type": "<skill_based|interest_based|collaborative>"
    }},
    ...
]

Consider factors like:
- User interests and preferences
- Learning objectives alignment
- Difficulty level match
- Duration compatibility
- Practical agricultural skills development
- Educational value for MFR students
"""
        return prompt
    
    def _parse_openai_response(self, response_text: str, activities: List[Activity]) -> List[Dict]:
        """Parse OpenAI response and map to activities."""
        try:
            # Extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            
            json_text = json_match.group()
            recommendations_data = json.loads(json_text)
            
            recommendations = []
            for rec_data in recommendations_data[:5]:  # Limit to top 5
                activity_index = rec_data.get("activity_id", 1) - 1
                if 0 <= activity_index < len(activities):
                    recommendations.append({
                        "activity": activities[activity_index],
                        "confidence_score": min(max(rec_data.get("confidence_score", 0.5), 0.0), 1.0),
                        "reasoning": rec_data.get("reasoning", "AI-generated recommendation"),
                        "recommendation_type": rec_data.get("recommendation_type", "interest_based")
                    })
            
            return recommendations
            
        except Exception as e:
            print(f"Error parsing OpenAI response: {e}")
            return self._rule_based_recommendations_fallback(activities)
    
    def _rule_based_recommendations(
        self, 
        user: User, 
        activities: List[Activity], 
        request: RecommendationRequest
    ) -> List[Dict]:
        """Fallback rule-based recommendation system."""
        recommendations = []
        
        # Filter activities based on user preferences
        filtered_activities = activities
        
        if request.preferred_difficulty:
            filtered_activities = [
                a for a in filtered_activities 
                if abs(a.difficulty_level - request.preferred_difficulty) <= 1
            ]
        
        if request.max_duration:
            filtered_activities = [
                a for a in filtered_activities 
                if a.duration_hours is None or a.duration_hours <= request.max_duration
            ]
        
        # Sort by difficulty level and featured status
        filtered_activities.sort(key=lambda x: (x.is_featured, -x.difficulty_level), reverse=True)
        
        # Create recommendations
        for i, activity in enumerate(filtered_activities[:5]):
            confidence_score = 0.8 if activity.is_featured else 0.6
            confidence_score -= i * 0.1  # Decrease confidence for lower ranked items
            
            recommendations.append({
                "activity": activity,
                "confidence_score": max(confidence_score, 0.3),
                "reasoning": "Rule-based recommendation based on user preferences and activity features",
                "recommendation_type": "skill_based"
            })
        
        return recommendations
    
    def _rule_based_recommendations_fallback(self, activities: List[Activity]) -> List[Dict]:
        """Basic fallback recommendations."""
        recommendations = []
        
        # Simply recommend featured activities first, then by difficulty
        sorted_activities = sorted(
            activities, 
            key=lambda x: (x.is_featured, x.difficulty_level), 
            reverse=True
        )
        
        for i, activity in enumerate(sorted_activities[:5]):
            recommendations.append({
                "activity": activity,
                "confidence_score": 0.5,
                "reasoning": "Basic recommendation based on activity popularity and difficulty",
                "recommendation_type": "collaborative"
            })
        
        return recommendations


# Singleton instance
openai_service = OpenAIService()