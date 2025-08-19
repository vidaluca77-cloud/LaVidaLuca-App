"""
API IA pour La Vida Luca
FastAPI backend pour les suggestions personnalisées et l'intelligence artificielle
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration
app = FastAPI(
    title="La Vida Luca - API IA",
    description="API d'intelligence artificielle pour les suggestions personnalisées d'activités",
    version="1.0.0"
)

# Configuration CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class UserProfile(BaseModel):
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []
    experience_level: str = "debutant"

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

class SuggestionRequest(BaseModel):
    user_profile: UserProfile
    limit: int = 5

# Endpoints
@app.get("/")
async def root():
    """Endpoint racine"""
    return {"message": "La Vida Luca - API IA", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check pour Render"""
    return {"status": "healthy", "service": "lavidaluca-ia-api"}

@app.post("/suggestions", response_model=List[Suggestion])
async def get_suggestions(request: SuggestionRequest):
    """
    Génère des suggestions personnalisées d'activités pour un utilisateur
    """
    try:
        # TODO: Implémenter la logique IA pour les suggestions
        # Pour l'instant, retourne des données de test
        
        mock_activity = Activity(
            id="1",
            slug="soins-animaux",
            title="Soins aux animaux",
            category="agri",
            summary="Nourrir, observer, nettoyer les espaces de vie.",
            duration_min=120,
            skill_tags=["douceur", "observation"],
            seasonality=["toutes"],
            safety_level=1,
            materials=["bottes", "gants"]
        )
        
        mock_suggestion = Suggestion(
            activity=mock_activity,
            score=0.85,
            reasons=[
                "Correspond à votre intérêt pour les animaux",
                "Niveau de sécurité adapté aux débutants",
                "Disponible toute l'année"
            ]
        )
        
        return [mock_suggestion]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération des suggestions: {str(e)}")

@app.post("/analyze-profile")
async def analyze_profile(profile: UserProfile):
    """
    Analyse un profil utilisateur et retourne des insights
    """
    try:
        # TODO: Implémenter l'analyse IA du profil
        
        insights = {
            "experience_assessment": "Débutant avec potentiel",
            "recommended_categories": ["agri", "nature"],
            "suggested_progression": [
                "Commencer par des activités de niveau 1",
                "Se concentrer sur l'observation et la douceur",
                "Progression vers les activités de transformation"
            ],
            "optimal_season": "printemps"
        }
        
        return insights
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse du profil: {str(e)}")

@app.get("/activities/categories")
async def get_categories():
    """Retourne les catégories d'activités disponibles"""
    return {
        "categories": [
            {"id": "agri", "name": "Agriculture", "description": "Activités agricoles et d'élevage"},
            {"id": "transfo", "name": "Transformation", "description": "Transformation des produits de la ferme"},
            {"id": "artisanat", "name": "Artisanat", "description": "Création et artisanat traditionnel"},
            {"id": "nature", "name": "Nature", "description": "Préservation et observation de la nature"},
            {"id": "social", "name": "Social", "description": "Animation et lien social"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))