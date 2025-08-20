from typing import Optional, List, Dict, Any
import openai
import json
from ..core.config import settings


class OpenAIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.client = None
    
    async def generate_activity_suggestions(
        self, 
        user_profile: Dict[str, Any], 
        user_preferences: Optional[str] = None,
        available_activities: List[Dict] = None,
        skills: List[Dict] = None
    ) -> List[Dict]:
        """Generate personalized activity suggestions using OpenAI."""
        
        if not self.client:
            return self._fallback_suggestions(user_profile, available_activities)
        
        # Prepare the context with user data
        context_parts = []
        
        # User profile information
        if user_profile:
            context_parts.append(f"User profile:")
            context_parts.append(f"- Level: {user_profile.get('current_level', 1)}")
            context_parts.append(f"- Experience points: {user_profile.get('experience_points', 0)}")
            context_parts.append(f"- Total activities completed: {user_profile.get('activities_completed', 0)}")
        
        # User skills
        if skills:
            skills_text = ", ".join([f"{skill['name']} (Level {skill['level']})" for skill in skills])
            context_parts.append(f"- Current skills: {skills_text}")
        
        # User preferences
        if user_preferences:
            context_parts.append(f"- Preferences: {user_preferences}")
        
        # Available activities
        if available_activities:
            context_parts.append(f"\nAvailable activities:")
            for i, activity in enumerate(available_activities[:15], 1):
                context_parts.append(
                    f"{i}. {activity['title']} ({activity['category']}) - "
                    f"Difficulty: {activity.get('difficulty_level', 'beginner')}, "
                    f"Points: {activity.get('points_reward', 10)}"
                )
        
        context = "\n".join(context_parts)
        
        prompt = f"""
        {context}
        
        As an AI educational advisor for agricultural and rural development programs, analyze the user's profile and recommend 3-5 activities that would best help them progress.
        
        Consider:
        - User's current level and experience
        - Skills they already have vs skills they need to develop
        - Appropriate difficulty progression
        - Variety of categories for well-rounded development
        
        Respond with a JSON array of recommendations. Each recommendation should include:
        - activity_index: The number (1-based) of the activity from the list above
        - score: A number between 0.1 and 1.0 indicating how good a match this is
        - reasons: An array of 2-3 specific reasons why this activity is recommended
        
        Example format:
        [
            {{"activity_index": 3, "score": 0.9, "reasons": ["Builds on your current gardening skills", "Appropriate for your experience level", "High practical value"]}},
            {{"activity_index": 7, "score": 0.8, "reasons": ["Introduces new category", "Good point reward for progression"]}}
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an AI assistant specialized in educational recommendations for agricultural and rural training programs. Always respond with valid JSON only."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse and validate the response
            try:
                suggestions_data = json.loads(content)
                suggestions = []
                
                for item in suggestions_data:
                    activity_index = item.get('activity_index', 1) - 1  # Convert to 0-based
                    score = item.get('score', 0.5)
                    reasons = item.get('reasons', ['Recommended by AI'])
                    
                    # Validate index
                    if 0 <= activity_index < len(available_activities):
                        suggestions.append({
                            'activity': available_activities[activity_index],
                            'score': min(max(score, 0.0), 1.0),
                            'reasons': reasons
                        })
                
                return suggestions[:5]  # Limit to 5 suggestions
                
            except json.JSONDecodeError:
                # If JSON parsing fails, fallback to simple suggestions
                return self._fallback_suggestions(user_profile, available_activities)
            
        except Exception as e:
            print(f"OpenAI API error: {str(e)}")
            return self._fallback_suggestions(user_profile, available_activities)
    
    def _fallback_suggestions(self, user_profile: Dict, available_activities: List[Dict]) -> List[Dict]:
        """Provide fallback suggestions when OpenAI is not available."""
        if not available_activities:
            return []
        
        suggestions = []
        user_level = user_profile.get('current_level', 1)
        completed_count = user_profile.get('activities_completed', 0)
        
        # Simple logic for fallback recommendations
        for activity in available_activities[:5]:
            score = 0.5
            reasons = ["Available activity"]
            
            # Adjust score based on difficulty and user level
            difficulty = activity.get('difficulty_level', 'beginner')
            if difficulty == 'beginner' and user_level <= 3:
                score += 0.3
                reasons.append("Appropriate for your level")
            elif difficulty == 'intermediate' and user_level >= 3:
                score += 0.2
                reasons.append("Good progression from your current level")
            elif difficulty == 'advanced' and user_level >= 5:
                score += 0.1
                reasons.append("Advanced challenge for experienced user")
            
            # Bonus for high point rewards
            points = activity.get('points_reward', 10)
            if points >= 20:
                score += 0.1
                reasons.append("High point reward")
            
            suggestions.append({
                'activity': activity,
                'score': min(score, 1.0),
                'reasons': reasons
            })
        
        # Sort by score
        suggestions.sort(key=lambda x: x['score'], reverse=True)
        return suggestions[:5]
    
    async def generate_activity_description(self, title: str, category: str, difficulty: str = "beginner") -> str:
        """Generate a detailed description for an activity using OpenAI."""
        
        if not self.client:
            return f"A {difficulty} level activity in {category}: {title}. This hands-on learning experience is designed to develop practical skills and knowledge in agricultural and rural development."
        
        prompt = f"""
        Create a detailed description for an educational activity titled "{title}" 
        in the category "{category}" with difficulty level "{difficulty}" for students in agricultural and rural training programs (MFR).
        
        Include:
        - Clear learning objectives (2-3 specific goals)
        - Step-by-step description of main activities
        - Expected outcomes and skills developed
        - Practical applications in rural/agricultural contexts
        - Estimated time commitment
        
        Keep it engaging and practical, around 150-200 words.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content creator specialized in agricultural and rural training programs. Create engaging, practical content that emphasizes hands-on learning."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"A {difficulty} level activity in {category}: {title}. This hands-on learning experience is designed to develop practical skills and knowledge in agricultural and rural development. Error generating detailed description: {str(e)}"
    
    async def generate_skill_suggestions(self, activity_title: str, category: str) -> List[str]:
        """Generate relevant skills that an activity should teach."""
        
        if not self.client:
            # Simple fallback based on category
            fallback_skills = {
                "agriculture": ["Jardinage Bio", "Compostage", "Observation"],
                "artisanat": ["Menuiserie", "Poterie", "Travail d'équipe"],
                "social": ["Communication", "Leadership", "Enseignement"],
                "nature": ["Botanique", "Écologie", "Orientation"]
            }
            return fallback_skills.get(category.lower(), ["Communication", "Observation"])
        
        prompt = f"""
        For an educational activity titled "{activity_title}" in the category "{category}", 
        suggest 2-4 specific skills that students would learn or develop.
        
        Consider skills relevant to agricultural and rural development such as:
        - Technical skills (gardening, animal care, craftsmanship)
        - Social skills (communication, teamwork, leadership)
        - Observation and analytical skills
        - Practical life skills
        
        Respond with a simple JSON array of skill names in French:
        ["Skill 1", "Skill 2", "Skill 3"]
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational consultant for agricultural training programs. Respond only with valid JSON."
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.5
            )
            
            content = response.choices[0].message.content.strip()
            skills = json.loads(content)
            return skills[:4]  # Limit to 4 skills
            
        except Exception as e:
            # Fallback
            fallback_skills = {
                "agriculture": ["Jardinage Bio", "Compostage"],
                "artisanat": ["Menuiserie", "Travail d'équipe"],
                "social": ["Communication", "Leadership"],
                "nature": ["Botanique", "Écologie"]
            }
            return fallback_skills.get(category.lower(), ["Communication", "Observation"])


# Global instance
openai_service = OpenAIService()