from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

app = FastAPI(
    title="La Vida Luca IA API",
    description="API pour l'intelligence artificielle du projet La Vida Luca",
    version="1.0.0"
)

# Configuration CORS
origins = [
    "http://localhost:3000",
    "https://localhost:3000",
]

# Ajouter les domaines Vercel depuis les variables d'environnement
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if allowed_origins and allowed_origins[0]:
    origins.extend([origin.strip() for origin in allowed_origins if origin.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de données
class ActivityRecommendation(BaseModel):
    id: str
    title: str
    category: str
    summary: str
    match_score: float
    reasons: List[str]

class UserProfile(BaseModel):
    skills: List[str]
    preferences: List[str]
    availability: List[str]
    experience_level: str = "debutant"

class RecommendationRequest(BaseModel):
    profile: UserProfile
    limit: Optional[int] = 5

@app.get("/")
async def root():
    return {
        "message": "La Vida Luca IA API",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/recommendations", response_model=List[ActivityRecommendation])
async def get_recommendations(request: RecommendationRequest):
    """
    Génère des recommandations d'activités basées sur le profil utilisateur.
    """
    # TODO: Implémenter la logique IA de recommandation
    # Pour l'instant, retour d'exemples statiques
    
    mock_recommendations = [
        ActivityRecommendation(
            id="1",
            title="Soins aux animaux",
            category="agri",
            summary="Contact, alimentation, observation du troupeau.",
            match_score=0.95,
            reasons=["Correspond à vos compétences en relationnel", "Activité adaptée aux débutants"]
        ),
        ActivityRecommendation(
            id="2", 
            title="Plantation de cultures",
            category="agri",
            summary="Semis, arrosage, paillage, suivi de plants.",
            match_score=0.88,
            reasons=["Activité saisonnière correspondant à vos disponibilités", "Développe les compétences en agriculture"]
        ),
        ActivityRecommendation(
            id="7",
            title="Fabrication de fromage",
            category="transfo",
            summary="Du lait au caillé : hygiène, moulage, affinage (découverte).",
            match_score=0.82,
            reasons=["Activité créative et artisanale", "Apprentissage de techniques traditionnelles"]
        )
    ]
    
    # Filtrer selon le nombre demandé
    return mock_recommendations[:request.limit]

@app.post("/profile/analyze")
async def analyze_profile(profile: UserProfile):
    """
    Analyse un profil utilisateur et suggère des améliorations.
    """
    # TODO: Implémenter l'analyse IA du profil
    
    suggestions = []
    
    if len(profile.skills) < 3:
        suggestions.append("Considérez ajouter plus de compétences pour de meilleures recommandations")
    
    if not profile.preferences:
        suggestions.append("Sélectionnez vos catégories préférées pour personnaliser les recommandations")
    
    return {
        "profile_completeness": min(100, (len(profile.skills) * 20 + len(profile.preferences) * 20 + len(profile.availability) * 15)),
        "suggestions": suggestions,
        "recommended_categories": ["agri", "nature", "social"] if not profile.preferences else profile.preferences
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)