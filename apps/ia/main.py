from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="La Vida Luca IA API",
    description="API IA pour les recommandations d'activités agricoles et pédagogiques",
    version="1.0.0"
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class UserProfile(BaseModel):
    skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]

class Activity(BaseModel):
    id: str
    slug: str
    title: str
    category: str
    summary: str
    duration_min: int
    skill_tags: List[str]
    seasonality: List[str]
    safety_level: int
    materials: List[str]

class Suggestion(BaseModel):
    activity: Activity
    score: float
    reasons: List[str]

class RecommendationRequest(BaseModel):
    user_profile: UserProfile
    max_suggestions: Optional[int] = 5

class RecommendationResponse(BaseModel):
    suggestions: List[Suggestion]
    timestamp: datetime

# Sample activities data (in production, this would come from database)
ACTIVITIES = [
    {
        "id": "1",
        "slug": "nourrissage-moutons",
        "title": "Nourrissage des moutons",
        "category": "agri",
        "summary": "Foin, granulés, eau : apprendre les besoins nutritionnels.",
        "duration_min": 45,
        "skill_tags": ["soin_animaux"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["bottes", "gants"]
    },
    {
        "id": "2",
        "slug": "tonte-entretien-troupeau",
        "title": "Tonte & entretien du troupeau",
        "category": "agri",
        "summary": "Hygiène, tonte (démo), soins courants.",
        "duration_min": 90,
        "skill_tags": ["elevage", "hygiene"],
        "seasonality": ["printemps"],
        "safety_level": 2,
        "materials": ["bottes", "gants"]
    }
]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "La Vida Luca IA API",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "api": "ok",
            "database": "pending",  # TODO: Add database health check
            "ai_model": "ok"
        }
    }

@app.get("/activities")
async def get_activities():
    """Get all available activities"""
    return {"activities": ACTIVITIES}

@app.post("/recommendations")
async def get_recommendations(request: RecommendationRequest) -> RecommendationResponse:
    """
    Get AI-powered activity recommendations based on user profile
    """
    try:
        # Simple recommendation algorithm (placeholder for actual AI)
        suggestions = []
        
        for activity_data in ACTIVITIES[:request.max_suggestions]:
            activity = Activity(**activity_data)
            
            # Calculate score based on profile matching
            score = calculate_recommendation_score(request.user_profile, activity)
            
            # Generate reasons
            reasons = generate_recommendation_reasons(request.user_profile, activity)
            
            suggestion = Suggestion(
                activity=activity,
                score=score,
                reasons=reasons
            )
            suggestions.append(suggestion)
        
        # Sort by score
        suggestions.sort(key=lambda x: x.score, reverse=True)
        
        return RecommendationResponse(
            suggestions=suggestions,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

def calculate_recommendation_score(profile: UserProfile, activity: Activity) -> float:
    """Calculate recommendation score (0.0 to 1.0)"""
    score = 0.0
    
    # Skill matching
    skill_matches = len(set(profile.skills) & set(activity.skill_tags))
    if skill_matches > 0:
        score += 0.4 * (skill_matches / max(len(activity.skill_tags), 1))
    
    # Preference matching
    if activity.category in profile.preferences:
        score += 0.3
    
    # Availability/seasonality matching
    season_matches = len(set(profile.availability) & set(activity.seasonality))
    if season_matches > 0 or 'toutes' in activity.seasonality:
        score += 0.3
    
    return min(score, 1.0)

def generate_recommendation_reasons(profile: UserProfile, activity: Activity) -> List[str]:
    """Generate human-readable reasons for recommendation"""
    reasons = []
    
    skill_matches = set(profile.skills) & set(activity.skill_tags)
    if skill_matches:
        reasons.append(f"Correspond à vos compétences: {', '.join(skill_matches)}")
    
    if activity.category in profile.preferences:
        reasons.append(f"Activité {activity.category} selon vos préférences")
    
    if 'toutes' in activity.seasonality:
        reasons.append("Disponible toute l'année")
    else:
        season_matches = set(profile.availability) & set(activity.seasonality)
        if season_matches:
            reasons.append(f"Disponible pendant: {', '.join(season_matches)}")
    
    if activity.safety_level == 1:
        reasons.append("Niveau de sécurité débutant")
    
    return reasons

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)