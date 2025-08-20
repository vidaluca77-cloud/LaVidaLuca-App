"""
OpenAI integration service for generating activity suggestions and agricultural consultations.
"""

import json
import openai
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

from ..config import settings


class SuggestionRequest(BaseModel):
    """Request schema for activity suggestions."""
    request: str = Field(..., description="User's request for activity suggestions")
    max_suggestions: int = Field(5, ge=1, le=10, description="Maximum number of suggestions")
    filters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional filters")


class AgriConsultationRequest(BaseModel):
    """Request schema for agricultural consultations."""
    question: str = Field(..., description="User's agricultural question")
    context: Optional[str] = Field(None, description="Additional context")
    user_location: Optional[str] = Field(None, description="User's location for localized advice")


async def get_agricultural_consultation(
    question: str,
    context: Optional[str] = None,
    user_location: Optional[str] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Get AI-powered agricultural consultation using OpenAI.
    
    Args:
        question: User's agricultural question
        context: Additional context for the question
        user_location: User's location for localized advice
        
    Returns:
        Tuple of (answer, metadata) where metadata contains AI model info, tokens used, etc.
    """
    if not settings.OPENAI_API_KEY:
        return _fallback_agricultural_response(question), {
            "model": "fallback",
            "tokens_used": "0",
            "confidence": "medium"
        }
    
    # Set up OpenAI client
    openai.api_key = settings.OPENAI_API_KEY
    
    # Build the prompt for agricultural consultation
    prompt = _build_agricultural_prompt(question, context, user_location)
    
    try:
        # Call OpenAI API
        response = await openai.chat.completions.create(
            model=settings.OPENAI_MODEL or "gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """Tu es un expert en agriculture durable, permaculture et jardinage écologique. 
                    Tu aides les agriculteurs, jardiniers et personnes intéressées par l'agriculture avec des conseils pratiques, 
                    scientifiquement fondés et respectueux de l'environnement. Tes réponses sont claires, structurées et adaptées 
                    au niveau de l'utilisateur. Tu privilégies toujours les méthodes naturelles et durables."""
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=settings.OPENAI_MAX_TOKENS or 1000,
            temperature=0.7,
        )
        
        # Extract response content
        answer = response.choices[0].message.content
        
        # Prepare metadata
        metadata = {
            "model": response.model,
            "tokens_used": str(response.usage.total_tokens) if response.usage else "unknown",
            "prompt_tokens": str(response.usage.prompt_tokens) if response.usage else "unknown",
            "completion_tokens": str(response.usage.completion_tokens) if response.usage else "unknown",
            "confidence": "high",
            "finish_reason": response.choices[0].finish_reason
        }
        
        return answer, metadata
        
    except Exception as e:
        # Fallback to predefined responses if OpenAI fails
        return _fallback_agricultural_response(question), {
            "model": "fallback",
            "tokens_used": "0",
            "confidence": "medium",
            "error": str(e)
        }


def _build_agricultural_prompt(
    question: str,
    context: Optional[str] = None,
    user_location: Optional[str] = None
) -> str:
    """Build the prompt for agricultural consultation."""
    
    location_info = f"\nLocalisation de l'utilisateur: {user_location}" if user_location else ""
    context_info = f"\nContexte supplémentaire: {context}" if context else ""
    
    prompt = f"""Question agricole: {question}{location_info}{context_info}

Veuillez fournir une réponse détaillée et pratique qui inclut:

1. **Réponse directe** à la question posée
2. **Conseils pratiques** étape par étape si applicable
3. **Considérations saisonnières** si pertinentes
4. **Alternatives écologiques** aux méthodes conventionnelles
5. **Ressources ou références** utiles si appropriées

Structurez votre réponse en utilisant des titres clairs et des listes à puces pour faciliter la lecture.
Adaptez le niveau technique à un public de jardiniers amateurs à confirmés.
Privilégiez toujours les méthodes durables et respectueuses de l'environnement."""
    
    return prompt


def _fallback_agricultural_response(question: str) -> str:
    """
    Provide fallback responses when OpenAI is not available.
    """
    question_lower = question.lower()
    
    if any(word in question_lower for word in ["sol", "terre", "ph", "compost"]):
        return """**Amélioration du sol - Conseils généraux**

1. **Analyse du sol** : Commencez par tester le pH et la structure de votre sol
2. **Apport de matière organique** : Ajoutez du compost bien décomposé
3. **Évitez le travail excessif** : Préservez la structure naturelle du sol
4. **Couvrez le sol** : Utilisez du paillis pour protéger et nourrir
5. **Rotation des cultures** : Alternez les familles de plantes

Pour des conseils plus spécifiques, n'hésitez pas à préciser votre type de sol et vos objectifs de culture."""

    elif any(word in question_lower for word in ["maladie", "ravageur", "parasite", "puceron", "traitement"]):
        return """**Gestion écologique des problèmes au jardin**

1. **Prévention** : Maintenir un sol sain et des plantes vigoureuses
2. **Observation régulière** : Inspectez vos plantes hebdomadairement
3. **Biodiversité** : Encouragez les auxiliaires naturels
4. **Traitements doux** : Savon noir, purin d'ortie, bicarbonate
5. **Rotation et associations** : Plantez des espèces complémentaires

Pour identifier un problème spécifique, décrivez les symptômes observés et les plantes affectées."""

    elif any(word in question_lower for word in ["arrosage", "irrigation", "eau", "sécheresse"]):
        return """**Gestion de l'eau au jardin**

1. **Arrosage matinal** : Privilégiez les heures fraîches
2. **Arrosage au pied** : Évitez de mouiller le feuillage
3. **Paillage** : Réduisez l'évaporation et conservez l'humidité
4. **Récupération d'eau** : Installez des systèmes de collecte d'eau de pluie
5. **Plantes adaptées** : Choisissez des variétés résistantes à la sécheresse

La fréquence d'arrosage dépend de votre climat, type de sol et stade de développement des plantes."""

    else:
        return f"""**Réponse à votre question : "{question}"**

Merci pour votre question agricole. Je suis là pour vous aider avec des conseils sur :

- **Le jardinage** et techniques de culture
- **La permaculture** et agriculture durable
- **La gestion du sol** et compostage
- **Les problèmes phytosanitaires** naturels
- **L'optimisation des récoltes**

Pour vous donner des conseils plus précis et adaptés, pourriez-vous :
1. Préciser votre contexte (jardin, potager, champ)
2. Indiquer votre région ou climat
3. Décrire plus en détail votre problématique

N'hésitez pas à reformuler votre question avec plus de détails !"""


async def get_activity_suggestions(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int = 5
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
                    "content": "You are an expert in educational activities and pedagogy for rural education (MFR - Maisons Familiales Rurales). You help students and educators find the most suitable learning activities based on their profile and needs."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
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
        return _fallback_suggestions(user_profile, user_request, available_activities, max_suggestions)


def _build_suggestion_prompt(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int
) -> str:
    """Build the prompt for OpenAI."""
    
    # Extract user info
    skills = user_profile.get('skills', [])
    interests = user_profile.get('interests', [])
    experience_level = user_profile.get('experience_level', 'beginner')
    location = user_profile.get('location', '')
    
    # Create activity summaries
    activity_summaries = []
    for i, activity in enumerate(available_activities):
        summary = f"{i+1}. {activity['title']} (Catégorie: {activity['category']}, Durée: {activity['duration_min']}min, Niveau: {activity.get('difficulty_level', 1)}/5)"
        if activity.get('skill_tags'):
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
    content: str, 
    available_activities: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Parse OpenAI response and match with activities."""
    suggestions = []
    
    try:
        # Try to parse as JSON
        parsed = json.loads(content)
        
        for item in parsed:
            activity_index = item.get('activity_index', 1) - 1  # Convert to 0-based index
            score = item.get('score', 0.5)
            reasons = item.get('reasons', ['Recommandé par IA'])
            
            # Validate index
            if 0 <= activity_index < len(available_activities):
                suggestions.append({
                    'activity': available_activities[activity_index],
                    'score': min(max(score, 0.0), 1.0),  # Ensure score is between 0 and 1
                    'reasons': reasons
                })
    
    except (json.JSONDecodeError, KeyError, IndexError):
        # If parsing fails, return empty list and let fallback handle it
        pass
    
    return suggestions


def _fallback_suggestions(
    user_profile: Dict[str, Any],
    user_request: str,
    available_activities: List[Dict[str, Any]],
    max_suggestions: int
) -> List[Dict[str, Any]]:
    """
    Fallback suggestion algorithm when OpenAI is not available.
    """
    suggestions = []
    user_skills = set(user_profile.get('skills', []))
    user_interests = set(user_profile.get('interests', []))
    user_experience = user_profile.get('experience_level', 'beginner')
    
    # Simple scoring based on matching
    for activity in available_activities:
        score = 0.3  # Base score
        reasons = []
        
        # Match skills
        activity_skills = set(activity.get('skill_tags', []))
        skill_overlap = user_skills & activity_skills
        if skill_overlap:
            score += 0.3
            reasons.append(f"Compétences correspondantes: {', '.join(list(skill_overlap)[:2])}")
        
        # Match interests with keywords/category
        activity_keywords = set(activity.get('keywords', []) + [activity.get('category', '')])
        interest_overlap = user_interests & activity_keywords
        if interest_overlap:
            score += 0.2
            reasons.append("Correspond à vos centres d'intérêt")
        
        # Experience level matching
        activity_difficulty = activity.get('difficulty_level', 1)
        if user_experience == 'beginner' and activity_difficulty <= 2:
            score += 0.1
            reasons.append("Adapté aux débutants")
        elif user_experience == 'intermediate' and 2 <= activity_difficulty <= 4:
            score += 0.1
            reasons.append("Niveau intermédiaire")
        elif user_experience == 'advanced' and activity_difficulty >= 3:
            score += 0.1
            reasons.append("Niveau avancé")
        
        # Featured activities get bonus
        if activity.get('is_featured'):
            score += 0.1
            reasons.append("Activité recommandée")
        
        if not reasons:
            reasons = ["Activité populaire"]
        
        suggestions.append({
            'activity': activity,
            'score': min(score, 1.0),
            'reasons': reasons
        })
    
    # Sort by score and return top suggestions
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions[:max_suggestions]