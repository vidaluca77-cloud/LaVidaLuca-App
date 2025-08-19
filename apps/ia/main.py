from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from pydantic import BaseModel
import os
from typing import List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour le projet La Vida Luca",
    version="1.0.0",
)

# Configuration CORS
origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not origins or origins == [""]:
    origins = ["http://localhost:3000", "https://*.vercel.app"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Models
class ActivitySuggestionRequest(BaseModel):
    user_skills: List[str]
    availability: List[str]
    location: str
    preferences: List[str]

class ActivitySuggestion(BaseModel):
    activity_id: str
    title: str
    score: float
    reasons: List[str]

class ChatRequest(BaseModel):
    message: str
    context: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    suggestions: List[str] = []

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "la-vida-luca-ia-api"}

# Activity suggestions endpoint
@app.post("/api/suggestions", response_model=List[ActivitySuggestion])
async def get_activity_suggestions(request: ActivitySuggestionRequest):
    """
    Génère des suggestions d'activités basées sur le profil utilisateur
    """
    # TODO: Implémenter la logique d'IA pour les suggestions
    # Pour l'instant, retourner des suggestions par défaut
    suggestions = [
        ActivitySuggestion(
            activity_id="1",
            title="Soins aux animaux",
            score=0.9,
            reasons=["Correspond à vos compétences en élevage", "Disponible dans votre région"]
        ),
        ActivitySuggestion(
            activity_id="4",
            title="Plantation de cultures",
            score=0.8,
            reasons=["Activité saisonnière adaptée", "Niveau débutant recommandé"]
        )
    ]
    return suggestions

# Chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Interface de chat avec l'IA pour répondre aux questions sur les activités
    """
    # TODO: Implémenter l'intégration avec OpenAI ou autre service d'IA
    # Pour l'instant, retourner une réponse par défaut
    response = ChatResponse(
        response="Je suis là pour vous aider avec vos questions sur les activités de La Vida Luca. Comment puis-je vous assister ?",
        suggestions=["Quelles sont les activités disponibles ?", "Comment puis-je participer ?", "Où se trouvent vos lieux d'action ?"]
    )
    return response

# Endpoint pour obtenir des informations sur une activité spécifique
@app.get("/api/activity/{activity_id}")
async def get_activity_info(activity_id: str):
    """
    Obtient des informations détaillées sur une activité spécifique
    """
    # TODO: Intégrer avec la base de données Supabase
    return {
        "id": activity_id,
        "status": "not_implemented",
        "message": "Endpoint en cours de développement"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))