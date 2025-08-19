from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import List, Optional

app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour La Vida Luca",
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
class ActivityRequest(BaseModel):
    user_profile: str
    interests: List[str]
    skill_level: str
    season: Optional[str] = None

class ActivityRecommendation(BaseModel):
    activity_id: str
    title: str
    confidence_score: float
    reasoning: str

class HealthResponse(BaseModel):
    status: str
    version: str

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Point de contrôle de santé pour Render"""
    return HealthResponse(status="healthy", version="1.0.0")

@app.get("/")
async def root():
    """Route racine de l'API"""
    return {
        "message": "La Vida Luca IA API",
        "version": "1.0.0",
        "status": "active"
    }

@app.post("/recommend-activities", response_model=List[ActivityRecommendation])
async def recommend_activities(request: ActivityRequest):
    """
    Recommander des activités basées sur le profil utilisateur
    """
    # TODO: Implémenter la logique d'IA pour les recommandations
    # Pour l'instant, retourne une recommandation exemple
    
    sample_recommendations = [
        ActivityRecommendation(
            activity_id="1",
            title="Soins aux animaux",
            confidence_score=0.95,
            reasoning="Basé sur votre profil et vos intérêts pour l'agriculture"
        ),
        ActivityRecommendation(
            activity_id="7",
            title="Fabrication de fromage",
            confidence_score=0.80,
            reasoning="Activité de transformation adaptée à votre niveau"
        )
    ]
    
    return sample_recommendations

@app.get("/activities/{activity_id}/safety-guide")
async def get_safety_guide(activity_id: str):
    """
    Générer un guide de sécurité personnalisé pour une activité
    """
    # TODO: Implémenter la génération de guides de sécurité
    return {
        "activity_id": activity_id,
        "safety_rules": [
            "Porter des équipements de protection",
            "Vérifier la présence d'un encadrant",
            "Suivre les consignes spécifiques à l'activité"
        ],
        "checklist": [
            "Matériel vérifié",
            "Formation reçue",
            "Conditions météo appropriées"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)