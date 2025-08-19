from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="La Vida Luca - API IA",
    description="API pour les fonctionnalités d'intelligence artificielle du projet La Vida Luca",
    version="1.0.0"
)

# Configuration CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = ["*"]  # Pour le développement

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles de données
class ActivityRecommendationRequest(BaseModel):
    user_skills: List[str]
    user_preferences: List[str]
    available_time: int
    location: Optional[str] = None

class ActivityRecommendation(BaseModel):
    activity_id: str
    title: str
    category: str
    score: float
    reasons: List[str]

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str]

# Routes principales
@app.get("/")
async def root():
    return {"message": "API IA La Vida Luca - Service opérationnel"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ia-api"}

@app.post("/recommend-activities", response_model=List[ActivityRecommendation])
async def recommend_activities(request: ActivityRecommendationRequest):
    """
    Recommande des activités basées sur le profil utilisateur
    """
    # TODO: Implémenter la logique de recommandation IA
    # Pour l'instant, retour d'exemples
    sample_recommendations = [
        ActivityRecommendation(
            activity_id="1",
            title="Soins aux animaux",
            category="agri",
            score=0.95,
            reasons=["Correspond à vos compétences en élevage", "Activité disponible dans votre région"]
        ),
        ActivityRecommendation(
            activity_id="4",
            title="Plantation de cultures",
            category="agri",
            score=0.87,
            reasons=["Adapté à votre niveau débutant", "Saison favorable"]
        )
    ]
    return sample_recommendations

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Interface de chat avec l'IA pour obtenir des conseils
    """
    # TODO: Intégrer OpenAI ou autre service d'IA
    response = ChatResponse(
        response="Merci pour votre question ! Je suis là pour vous aider avec les activités de La Vida Luca.",
        suggestions=[
            "Quelles activités sont disponibles ce mois-ci ?",
            "Comment puis-je commencer en agriculture ?",
            "Quels sont les prérequis pour les activités artisanales ?"
        ]
    )
    return response

@app.get("/activities/suggest/{activity_id}")
async def get_activity_suggestions(activity_id: str):
    """
    Obtient des suggestions personnalisées pour une activité spécifique
    """
    # TODO: Implémenter la logique de suggestions
    return {
        "activity_id": activity_id,
        "suggestions": [
            "Préparez des vêtements adaptés",
            "Consultez la météo avant de venir",
            "Apportez votre motivation et votre curiosité !"
        ],
        "preparation_tips": [
            "Lecture recommandée sur l'agriculture durable",
            "Vidéos d'introduction disponibles"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)