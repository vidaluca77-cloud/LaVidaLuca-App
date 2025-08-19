from typing import Optional, Dict, Any, List
import openai
import json
from ..core.config import settings


class OpenAIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
    
    def generate_activity_suggestions(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized activity suggestions using OpenAI."""
        
        if not self.client:
            return []
        
        try:
            # Format user preferences for prompt
            preferences_text = self._format_user_preferences(user_preferences)
            
            prompt = f"""
            Based on the following user preferences:
            {preferences_text}
            
            Suggest 3-5 educational activities that would be most beneficial for this user's learning.
            
            Provide suggestions in JSON format:
            {{
                "suggestions": [
                    {{
                        "title": "Activity Name",
                        "description": "Brief description",
                        "category": "technology|sports|arts|nature|science",
                        "difficulty_level": "beginner|intermediate|advanced",
                        "duration_minutes": 60
                    }}
                ]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an AI assistant specialized in educational recommendations."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            parsed_response = json.loads(content)
            
            # Validate and return suggestions
            suggestions = parsed_response.get("suggestions", [])
            validated_suggestions = [
                suggestion for suggestion in suggestions
                if self._validate_suggestion_format(suggestion)
            ]
            
            return validated_suggestions
            
        except Exception:
            return []
    
    def analyze_activity_content(self, activity_content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze activity content using OpenAI."""
        
        if not self.client:
            return {}
        
        try:
            prompt = f"""
            Analyze the following activity:
            Title: {activity_content.get('title', '')}
            Description: {activity_content.get('description', '')}
            Category: {activity_content.get('category', '')}
            
            Provide analysis in JSON format:
            {{
                "analysis": {{
                    "difficulty_assessment": "description of difficulty",
                    "learning_objectives": ["objective1", "objective2"],
                    "estimated_duration": 45,
                    "required_skills": ["skill1", "skill2"]
                }}
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content analyzer."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.6
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception:
            return {}
    
    def _format_user_preferences(self, preferences: Dict[str, Any]) -> str:
        """Format user preferences for OpenAI prompts."""
        formatted_lines = []
        
        for key, value in preferences.items():
            if isinstance(value, list):
                formatted_lines.append(f"{key}: {', '.join(value)}")
            else:
                formatted_lines.append(f"{key}: {value}")
        
        return "\n".join(formatted_lines)
    
    def _validate_suggestion_format(self, suggestion: Dict[str, Any]) -> bool:
        """Validate that suggestion has required fields."""
        required_fields = ["title", "description", "category", "difficulty_level", "duration_minutes"]
        return all(field in suggestion for field in required_fields)