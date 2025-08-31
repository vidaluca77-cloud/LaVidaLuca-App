from typing import Optional
import openai
from ..core.config import settings


class OpenAIService:
    def __init__(self):
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY

    async def generate_activity_suggestions(
        self,
        user_profile: str,
        user_preferences: Optional[str] = None,
        available_activities: list = None,
    ) -> list:
        """Generate personalized activity suggestions using OpenAI."""

        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")

        # Prepare the prompt
        context = f"User profile: {user_profile}"
        if user_preferences:
            context += f"\nUser preferences: {user_preferences}"

        if available_activities:
            activities_list = "\n".join(
                [
                    f"- {activity['title']} ({activity['category']}): {activity['description'][:100]}..."
                    for activity in available_activities[:10]
                ]
            )
            context += f"\n\nAvailable activities:\n{activities_list}"

        prompt = f"""
        {context}
        
        Based on the user profile and available activities, suggest 3-5 educational activities 
        that would be most beneficial for this user's learning in agricultural and rural development.
        
        Provide suggestions in JSON format:
        [
            {{"activity_title": "Activity Name", "reason": "Brief explanation why this is suitable"}},
            ...
        ]
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an AI assistant specialized in educational recommendations for agricultural and rural training programs.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    async def generate_activity_description(self, title: str, category: str) -> str:
        """Generate a detailed description for an activity using OpenAI."""

        if not settings.OPENAI_API_KEY:
            return f"Description for {title} in {category} category."

        prompt = f"""
        Create a detailed description for an educational activity titled "{title}" 
        in the category "{category}" for students in agricultural and rural training programs (MFR).
        
        Include:
        - Learning objectives
        - Brief description of activities
        - Expected outcomes
        
        Keep it concise but informative (max 200 words).
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an educational content creator for agricultural and rural training programs.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=300,
                temperature=0.6,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Failed to generate description: {str(e)}"


# Global instance
openai_service = OpenAIService()
