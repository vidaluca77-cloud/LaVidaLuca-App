from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user_id
from app.models.user import User
from app.models.activity import Activity
from app.schemas.activity import ActivityResponse
import openai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize OpenAI client
if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY


def calculate_activity_matching(user: User, activities: List[Activity]) -> List[dict]:
    """Calculate matching score between user and activities"""
    suggestions = []
    
    for activity in activities:
        score = 0
        reasons = []
        
        # Skills matching
        if user.skills and activity.skill_tags:
            common_skills = set(user.skills) & set(activity.skill_tags)
            if common_skills:
                score += len(common_skills) * 15
                reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Category preferences
        if user.preferences and activity.category in user.preferences:
            score += 25
            category_names = {
                'agri': 'Agriculture',
                'transfo': 'Transformation',
                'artisanat': 'Artisanat',
                'nature': 'Environnement',
                'social': 'Animation'
            }
            reasons.append(f"Catégorie préférée : {category_names.get(activity.category, activity.category)}")
        
        # Duration preference (shorter activities for beginners)
        if activity.duration_min <= 90:
            score += 10
            reasons.append("Durée adaptée pour débuter")
        
        # Safety level
        if activity.safety_level <= 2:
            score += 10
            if activity.safety_level == 1:
                reasons.append("Activité sans risque particulier")
        
        # Availability matching (simulation)
        if user.availability and ('weekend' in user.availability or 'semaine' in user.availability):
            score += 15
            reasons.append("Compatible avec vos disponibilités")
        
        suggestions.append({
            'activity': activity,
            'score': score,
            'reasons': reasons
        })
    
    # Sort by score (descending)
    suggestions.sort(key=lambda x: x['score'], reverse=True)
    return suggestions


async def get_ai_recommendations(user: User, activities: List[Activity]) -> str:
    """Get AI-powered recommendations using OpenAI"""
    if not settings.OPENAI_API_KEY:
        return "AI recommendations not available (API key not configured)"
    
    try:
        user_profile = f"""
        Compétences: {', '.join(user.skills) if user.skills else 'Aucune'}
        Disponibilités: {', '.join(user.availability) if user.availability else 'Non spécifiées'}
        Localisation: {user.location or 'Non spécifiée'}
        Préférences: {', '.join(user.preferences) if user.preferences else 'Aucune'}
        """
        
        activities_summary = "\n".join([
            f"- {activity.title} ({activity.category}): {activity.summary}"
            for activity in activities[:10]  # Limit to first 10 for context
        ])
        
        prompt = f"""
        En tant qu'expert en formation agricole et artisanale, analysez ce profil utilisateur et recommandez les meilleures activités:

        Profil utilisateur:
        {user_profile}

        Activités disponibles:
        {activities_summary}

        Donnez 3 recommandations personnalisées avec justifications courtes (2-3 phrases max par recommandation).
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Vous êtes un expert en formation agricole et artisanale pour le projet La Vida Luca."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return "Erreur lors de la génération des recommandations IA"


@router.get("/", response_model=List[dict])
async def get_recommendations(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get personalized activity recommendations for current user"""
    # Get user profile
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get all activities
    activities = db.query(Activity).all()
    if not activities:
        return []
    
    # Calculate matching scores
    suggestions = calculate_activity_matching(user, activities)
    
    # Return top 10 suggestions with activity details
    top_suggestions = suggestions[:10]
    result = []
    
    for suggestion in top_suggestions:
        result.append({
            "activity": ActivityResponse.from_orm(suggestion['activity']).dict(),
            "score": suggestion['score'],
            "reasons": suggestion['reasons']
        })
    
    logger.info(f"Generated {len(result)} recommendations for user {user.email}")
    return result


@router.get("/ai", response_model=dict)
async def get_ai_recommendations_endpoint(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """Get AI-powered activity recommendations"""
    # Get user profile
    user = db.query(User).filter(User.id == current_user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get activities for context
    activities = db.query(Activity).limit(20).all()  # Limit for API efficiency
    
    # Get AI recommendations
    ai_recommendations = await get_ai_recommendations(user, activities)
    
    logger.info(f"Generated AI recommendations for user {user.email}")
    return {
        "recommendations": ai_recommendations,
        "user_profile": {
            "skills": user.skills,
            "availability": user.availability,
            "preferences": user.preferences
        }
    }