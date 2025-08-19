import openai
from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.schemas import UserBase, ActivityResponse
import json


class OpenAIService:
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        
    async def generate_recommendations(
        self, 
        user_profile: UserBase, 
        activities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Generate AI-powered activity recommendations based on user profile.
        """
        if not settings.openai_api_key:
            # Fallback to rule-based recommendations if OpenAI is not configured
            return self._rule_based_recommendations(user_profile, activities)
        
        try:
            # Prepare the prompt
            prompt = self._build_recommendation_prompt(user_profile, activities)
            
            # Call OpenAI API
            client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in agricultural education and youth development, specialized in matching activities to student profiles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            # Parse the response
            recommendation_text = response.choices[0].message.content
            return self._parse_ai_recommendations(recommendation_text, activities)
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based recommendations
            return self._rule_based_recommendations(user_profile, activities)
    
    def _build_recommendation_prompt(self, user_profile: UserBase, activities: List[Dict[str, Any]]) -> str:
        """Build the prompt for OpenAI recommendation."""
        activities_text = ""
        for i, activity in enumerate(activities):
            activities_text += f"{i+1}. {activity['title']} ({activity['category']})\n"
            activities_text += f"   Summary: {activity['summary']}\n"
            activities_text += f"   Duration: {activity['duration_min']} min\n"
            activities_text += f"   Skills: {', '.join(activity['skill_tags'])}\n"
            activities_text += f"   Safety: Level {activity['safety_level']}\n"
            activities_text += f"   Season: {', '.join(activity['seasonality'])}\n\n"
        
        prompt = f"""
As an expert in agricultural education, recommend the top 5 activities for this student profile:

STUDENT PROFILE:
- Skills: {', '.join(user_profile.skills)}
- Availability: {', '.join(user_profile.availability)}
- Location: {user_profile.location}
- Interests: {', '.join(user_profile.preferences)}

AVAILABLE ACTIVITIES:
{activities_text}

Please provide:
1. Top 5 recommended activities (by number)
2. For each, a score from 0-100
3. 2-3 specific reasons why it matches the student

Format your response as JSON:
{{
  "recommendations": [
    {{
      "activity_number": 1,
      "score": 85,
      "reasons": ["reason 1", "reason 2"]
    }}
  ]
}}
"""
        return prompt
    
    def _parse_ai_recommendations(self, response_text: str, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse OpenAI response into structured recommendations."""
        try:
            # Try to extract JSON from the response
            response_data = json.loads(response_text)
            recommendations = []
            
            for rec in response_data.get("recommendations", []):
                activity_number = rec.get("activity_number", 1) - 1  # Convert to 0-based index
                if 0 <= activity_number < len(activities):
                    recommendations.append({
                        "activity": activities[activity_number],
                        "score": rec.get("score", 50),
                        "reasons": rec.get("reasons", ["AI recommendation"])
                    })
            
            return recommendations
            
        except (json.JSONDecodeError, KeyError, IndexError):
            # Fallback if parsing fails
            return self._rule_based_recommendations(
                UserBase(
                    email="fallback@example.com",
                    username="fallback",
                    skills=[],
                    availability=[],
                    preferences=[]
                ), 
                activities
            )
    
    def _rule_based_recommendations(self, user_profile: UserBase, activities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fallback rule-based recommendation system."""
        recommendations = []
        
        for activity in activities:
            score = 0
            reasons = []
            
            # Skill matching
            skill_matches = set(user_profile.skills) & set(activity.get('skill_tags', []))
            if skill_matches:
                score += len(skill_matches) * 20
                reasons.append(f"Matches your skills: {', '.join(skill_matches)}")
            
            # Category preference
            if activity.get('category') in user_profile.preferences:
                score += 25
                category_names = {
                    'agri': 'Agriculture',
                    'transfo': 'Transformation',
                    'artisanat': 'Artisanat',
                    'nature': 'Environnement',
                    'social': 'Animation'
                }
                reasons.append(f"Matches your interest in: {category_names.get(activity.get('category'), activity.get('category'))}")
            
            # Duration suitability
            if activity.get('duration_min', 0) <= 90:
                score += 10
                reasons.append("Good duration for beginners")
            
            # Safety level
            if activity.get('safety_level', 3) <= 2:
                score += 10
                if activity.get('safety_level') == 1:
                    reasons.append("Low risk activity")
            
            # Availability matching (simplified)
            if any(avail in ['weekend', 'semaine'] for avail in user_profile.availability):
                score += 15
                reasons.append("Fits your schedule")
            
            if not reasons:
                reasons = ["Good learning opportunity"]
            
            recommendations.append({
                "activity": activity,
                "score": min(score, 100),  # Cap at 100
                "reasons": reasons[:3]  # Limit to 3 reasons
            })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:5]


# Global service instance
openai_service = OpenAIService()