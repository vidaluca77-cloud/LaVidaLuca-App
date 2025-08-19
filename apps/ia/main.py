from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="La Vida Luca IA API",
    description="API IA pour la plateforme La Vida Luca",
    version="1.0.0"
)

# Configuration CORS
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
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
    score: int
    reasons: List[str]

class MatchingRequest(BaseModel):
    profile: UserProfile

class MatchingResponse(BaseModel):
    suggestions: List[Suggestion]

# Données des activités (temporaire - à terme dans la DB)
ACTIVITIES = [
    {
        "id": "1", "slug": "nourrir-animaux", "title": "Nourrir les animaux",
        "category": "agri", "summary": "Distribution alimentation, vérifier abreuvoirs, observer comportements.",
        "duration_min": 60, "skill_tags": ["observation", "douceur"], "seasonality": ["toutes"],
        "safety_level": 1, "materials": ["bottes"]
    },
    {
        "id": "2", "slug": "collecte-oeufs", "title": "Collecte des œufs",
        "category": "agri", "summary": "Ramasser délicatement, nettoyer si besoin, stockage correct.",
        "duration_min": 30, "skill_tags": ["douceur", "organisation"], "seasonality": ["toutes"],
        "safety_level": 1, "materials": []
    }
    # Ajout des autres activités...
]

@app.get("/")
async def root():
    return {"message": "La Vida Luca IA API - Opérationnelle"}

@app.post("/matching", response_model=MatchingResponse)
async def get_activity_matching(request: MatchingRequest):
    """
    Système de matching IA pour recommander des activités 
    basé sur le profil utilisateur
    """
    profile = request.profile
    suggestions = []
    
    for activity_data in ACTIVITIES:
        activity = Activity(**activity_data)
        score = 0
        reasons = []
        
        # Calcul du score basé sur les compétences communes
        common_skills = set(activity.skill_tags) & set(profile.skills)
        if common_skills:
            score += len(common_skills) * 15
            reasons.append(f"Compétences correspondantes : {', '.join(common_skills)}")
        
        # Préférences de catégories
        if activity.category in profile.preferences:
            score += 25
            reasons.append(f"Catégorie préférée : {activity.category}")
        
        # Disponibilité selon la saison
        if "toutes" in activity.seasonality or any(season in profile.availability for season in activity.seasonality):
            score += 10
            reasons.append("Disponibilité compatible")
        
        if score > 0:
            suggestions.append(Suggestion(
                activity=activity,
                score=score,
                reasons=reasons
            ))
    
    # Trier par score décroissant
    suggestions.sort(key=lambda x: x.score, reverse=True)
    
    return MatchingResponse(suggestions=suggestions[:5])

@app.get("/activities", response_model=List[Activity])
async def get_activities():
    """Récupère toutes les activités disponibles"""
    return [Activity(**activity) for activity in ACTIVITIES]

@app.get("/activities/{activity_id}", response_model=Activity)
async def get_activity(activity_id: str):
    """Récupère une activité spécifique par ID"""
    activity_data = next((a for a in ACTIVITIES if a["id"] == activity_id), None)
    if not activity_data:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    return Activity(**activity_data)

@app.get("/health")
async def health_check():
    """Endpoint de santé pour le monitoring"""
    return {"status": "healthy", "service": "la-vida-luca-ia"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)