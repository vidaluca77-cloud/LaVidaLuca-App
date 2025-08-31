"""
OpenAI integration service for generating activity suggestions.
"""

import json
import openai
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from ..config import settings


class SuggestionRequest(BaseModel):
    """Request schema for activity suggestions."""

    request: str = Field(..., description="User's request for activity suggestions")
    max_suggestions: int = Field(
        5, ge=1, le=10, description="Maximum number of suggestions"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Additional filters"
    )


async def get_activity_suggestions(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int = 5,
) -> List[Dict[str, Any]]:
    """
    Generate personalized activity suggestions using OpenAI.

    Args:
        user_profile: User's profile information
        user_request: User's specific request
        available_activities: List of available activities
        max_suggestions: Maximum number of suggestions to return

    Returns:
        List of activity suggestions with scores and reasons
    """
    # Set up OpenAI client
    openai.api_key = settings.OPENAI_API_KEY

    # Prepare the prompt
    prompt = _build_suggestion_prompt(
        user_profile, user_request, available_activities, max_suggestions
    )

    try:
        # Call OpenAI API
        response = await openai.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert in educational activities and pedagogy for rural education (MFR - Maisons Familiales Rurales). You help students and educators find the most suitable learning activities based on their profile and needs.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=settings.OPENAI_MAX_TOKENS,
            temperature=0.7,
        )

        # Parse the response
        content = response.choices[0].message.content
        suggestions = _parse_openai_response(content, available_activities)

        return suggestions[:max_suggestions]

    except Exception as e:
        # Fallback to simple matching if OpenAI fails
        return _fallback_suggestions(
            user_profile, user_request, available_activities, max_suggestions
        )


def _build_suggestion_prompt(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int,
) -> str:
    """Build the prompt for OpenAI."""

    # Extract user info
    skills = user_profile.get("skills", [])
    interests = user_profile.get("interests", [])
    experience_level = user_profile.get("experience_level", "beginner")
    location = user_profile.get("location", "")

    # Create activity summaries
    activity_summaries = []
    for i, activity in enumerate(available_activities):
        summary = f"{i+1}. {activity['title']} (Catégorie: {activity['category']}, Durée: {activity['duration_min']}min, Niveau: {activity.get('difficulty_level', 1)}/5)"
        if activity.get("skill_tags"):
            summary += f" - Compétences: {', '.join(activity['skill_tags'][:3])}"
        activity_summaries.append(summary)

    prompt = f"""
Demande de l'utilisateur: "{user_request}"

Profil de l'utilisateur:
- Compétences: {', '.join(skills) if skills else 'Non spécifiées'}
- Centres d'intérêt: {', '.join(interests) if interests else 'Non spécifiés'}
- Niveau d'expérience: {experience_level}
- Localisation: {location if location else 'Non spécifiée'}

Activités disponibles:
{chr(10).join(activity_summaries[:20])}  # Limit to first 20 activities

Veuillez recommander jusqu'à {max_suggestions} activités les plus pertinentes pour cet utilisateur.

Pour chaque recommandation, fournissez:
1. Le numéro de l'activité (de la liste ci-dessus)
2. Un score de pertinence (0.0 à 1.0)
3. 2-3 raisons courtes expliquant pourquoi cette activité est recommandée

Format de réponse JSON attendu:
[
  {{
    "activity_index": 1,
    "score": 0.85,
    "reasons": ["Raison 1", "Raison 2"]
  }}
]
"""

    return prompt


def _parse_openai_response(
    content: str, available_activities: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Parse OpenAI response and match with activities."""
    suggestions = []

    try:
        # Try to parse as JSON
        parsed = json.loads(content)

        for item in parsed:
            activity_index = (
                item.get("activity_index", 1) - 1
            )  # Convert to 0-based index
            score = item.get("score", 0.5)
            reasons = item.get("reasons", ["Recommandé par IA"])

            # Validate index
            if 0 <= activity_index < len(available_activities):
                suggestions.append(
                    {
                        "activity": available_activities[activity_index],
                        "score": min(
                            max(score, 0.0), 1.0
                        ),  # Ensure score is between 0 and 1
                        "reasons": reasons,
                    }
                )

    except (json.JSONDecodeError, KeyError, IndexError):
        # If parsing fails, return empty list and let fallback handle it
        pass

    return suggestions


def _fallback_suggestions(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int,
) -> List[Dict[str, Any]]:
    """
    Fallback suggestion algorithm when OpenAI is not available.
    """
    suggestions = []
    user_skills = set(user_profile.get("skills", []))
    user_interests = set(user_profile.get("interests", []))
    user_experience = user_profile.get("experience_level", "beginner")

    # Simple scoring based on matching
    for activity in available_activities:
        score = 0.3  # Base score
        reasons = []

        # Match skills
        activity_skills = set(activity.get("skill_tags", []))
        skill_overlap = user_skills & activity_skills
        if skill_overlap:
            score += 0.3
            reasons.append(
                f"Compétences correspondantes: {', '.join(list(skill_overlap)[:2])}"
            )

        # Match interests with keywords/category
        activity_keywords = set(
            activity.get("keywords", []) + [activity.get("category", "")]
        )
        interest_overlap = user_interests & activity_keywords
        if interest_overlap:
            score += 0.2
            reasons.append("Correspond à vos centres d'intérêt")

        # Experience level matching
        activity_difficulty = activity.get("difficulty_level", 1)
        if user_experience == "beginner" and activity_difficulty <= 2:
            score += 0.1
            reasons.append("Adapté aux débutants")
        elif user_experience == "intermediate" and 2 <= activity_difficulty <= 4:
            score += 0.1
            reasons.append("Niveau intermédiaire")
        elif user_experience == "advanced" and activity_difficulty >= 3:
            score += 0.1
            reasons.append("Niveau avancé")

        # Featured activities get bonus
        if activity.get("is_featured"):
            score += 0.1
            reasons.append("Activité recommandée")

        if not reasons:
            reasons = ["Activité populaire"]

        suggestions.append(
            {"activity": activity, "score": min(score, 1.0), "reasons": reasons}
        )

    # Sort by score and return top suggestions
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return suggestions[:max_suggestions]
