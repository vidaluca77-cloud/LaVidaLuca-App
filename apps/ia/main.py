"""
FastAPI Backend pour l'IA La Vida Luca
Endpoints: /health, /guide, /chat
"""

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# Configuration logging
logging.basicConfig(level=getattr(logging, os.getenv("LOG_LEVEL", "INFO")))
logger = logging.getLogger(__name__)

# Configuration CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# Initialisation FastAPI
app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour le projet La Vida Luca",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models Pydantic
class HealthResponse(BaseModel):
    status: str = "healthy"
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = "1.0.0"

class UserProfile(BaseModel):
    skills: List[str] = []
    availability: List[str] = []
    location: str = ""
    preferences: List[str] = []

class GuideRequest(BaseModel):
    profile: UserProfile
    activity_id: Optional[str] = None
    category: Optional[str] = None

class GuideResponse(BaseModel):
    suggestions: List[Dict[str, Any]]
    safety_guide: Dict[str, Any]
    personalized_tips: List[str]

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime = Field(default_factory=datetime.now)
    context_used: bool = False

# Base de données simulée des activités
ACTIVITIES_DB = [
    {
        "id": "1",
        "slug": "nourrir-poules",
        "title": "Nourrir les poules",
        "category": "agri",
        "summary": "Donner à manger aux poules, ramasser les œufs, nettoyer.",
        "duration_min": 30,
        "skill_tags": ["elevage", "hygiene", "soins_animaux"],
        "seasonality": ["toutes"],
        "safety_level": 1,
        "materials": ["gants", "seau"]
    },
    {
        "id": "2",
        "slug": "preparer-sol",
        "title": "Préparer le sol",
        "category": "agri",
        "summary": "Bêcher, retourner, aérer la terre pour les cultures.",
        "duration_min": 60,
        "skill_tags": ["sol", "endurance"],
        "seasonality": ["printemps", "automne"],
        "safety_level": 2,
        "materials": ["bêche", "gants", "chaussures_sécurité"]
    },
    {
        "id": "3",
        "slug": "planter-graines",
        "title": "Planter des graines",
        "category": "agri",
        "summary": "Semer, repiquer, arroser selon la saison.",
        "duration_min": 45,
        "skill_tags": ["plantes", "precision", "patience"],
        "seasonality": ["printemps", "été"],
        "safety_level": 1,
        "materials": ["gants", "arrosoir"]
    }
]

# Fonctions utilitaires
def calculate_compatibility_score(profile: UserProfile, activity: Dict[str, Any]) -> float:
    """Calcule un score de compatibilité entre un profil utilisateur et une activité"""
    score = 0.0
    
    # Score basé sur les compétences
    matching_skills = set(profile.skills) & set(activity["skill_tags"])
    if activity["skill_tags"]:
        skill_score = len(matching_skills) / len(activity["skill_tags"])
        score += skill_score * 0.4
    
    # Score basé sur les préférences de catégorie
    if activity["category"] in profile.preferences:
        score += 0.3
    
    # Score basé sur la disponibilité (simplifié)
    if profile.availability:
        score += 0.2
    
    # Bonus pour activités de niveau de sécurité approprié
    if activity["safety_level"] == 1:
        score += 0.1
    
    return min(score, 1.0)

def generate_safety_guide(activity: Dict[str, Any]) -> Dict[str, Any]:
    """Génère un guide de sécurité pour une activité"""
    base_rules = [
        "Respecter les consignes de l'encadrant en permanence",
        "Porter les équipements de protection indiqués",
        "Signaler immédiatement tout problème ou incident"
    ]
    
    base_checklist = [
        "Vérifier la présence de l'encadrant",
        "S'assurer d'avoir tous les matériels nécessaires",
        "Prendre connaissance des consignes de sécurité"
    ]
    
    if activity["safety_level"] >= 2:
        base_rules.extend([
            "Ne jamais agir seul, toujours en binôme minimum",
            "Vérifier deux fois avant d'utiliser un outil"
        ])
        base_checklist.extend([
            "Vérifier l'état des outils avant utilisation",
            "S'assurer de la présence d'une trousse de premiers secours"
        ])
    
    return {
        "rules": base_rules,
        "checklist": base_checklist,
        "safety_level": activity["safety_level"],
        "required_materials": activity["materials"]
    }

def generate_personalized_tips(profile: UserProfile, activity: Dict[str, Any]) -> List[str]:
    """Génère des conseils personnalisés basés sur le profil"""
    tips = []
    
    # Conseils basés sur les compétences
    if "patience" in profile.skills and "precision" in activity["skill_tags"]:
        tips.append("Votre patience sera un atout pour cette activité de précision")
    
    if "equipe" in profile.skills:
        tips.append("N'hésitez pas à proposer votre aide aux autres participants")
    
    # Conseils basés sur la disponibilité
    if "matin" in profile.availability:
        tips.append("Cette activité est idéale le matin quand vous êtes plus énergique")
    
    # Conseils généraux
    tips.append("Prenez le temps d'observer avant d'agir")
    tips.append("N'hésitez pas à poser des questions à l'encadrant")
    
    return tips

# Endpoints
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Endpoint de vérification de santé de l'API"""
    logger.info("Health check requested")
    return HealthResponse()

@app.post("/guide", response_model=GuideResponse)
async def get_personalized_guide(request: GuideRequest):
    """Endpoint pour obtenir un guide personnalisé basé sur le profil utilisateur"""
    try:
        logger.info(f"Guide request for profile: {request.profile}")
        
        # Filtrer les activités selon la catégorie si spécifiée
        activities = ACTIVITIES_DB
        if request.category:
            activities = [a for a in activities if a["category"] == request.category]
        
        # Calculer les scores de compatibilité
        scored_activities = []
        for activity in activities:
            score = calculate_compatibility_score(request.profile, activity)
            activity_with_score = {**activity, "compatibility_score": score}
            scored_activities.append(activity_with_score)
        
        # Trier par score et prendre les 3 meilleures
        suggestions = sorted(scored_activities, key=lambda x: x["compatibility_score"], reverse=True)[:3]
        
        # Générer le guide de sécurité pour la première suggestion
        safety_guide = {}
        if suggestions:
            safety_guide = generate_safety_guide(suggestions[0])
        
        # Générer des conseils personnalisés
        personalized_tips = []
        if suggestions:
            personalized_tips = generate_personalized_tips(request.profile, suggestions[0])
        
        response = GuideResponse(
            suggestions=suggestions,
            safety_guide=safety_guide,
            personalized_tips=personalized_tips
        )
        
        logger.info(f"Generated guide with {len(suggestions)} suggestions")
        return response
        
    except Exception as e:
        logger.error(f"Error generating guide: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du guide")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """Endpoint de chat avec l'IA pour des questions sur les activités"""
    try:
        logger.info(f"Chat message received: {message.message[:50]}...")
        
        # Simulation d'une réponse IA intelligente
        user_message = message.message.lower()
        
        # Réponses contextuelles simples
        if "sécurité" in user_message or "danger" in user_message:
            response_text = (
                "La sécurité est notre priorité ! Toutes nos activités sont encadrées par des professionnels. "
                "Portez toujours les équipements de protection recommandés et n'hésitez pas à poser des questions."
            )
        elif "activité" in user_message or "que faire" in user_message:
            response_text = (
                "Nous proposons 30 activités variées dans 4 catégories : agriculture, artisanat, nature et social. "
                "Renseignez votre profil pour recevoir des suggestions personnalisées adaptées à vos compétences !"
            )
        elif "temps" in user_message or "durée" in user_message:
            response_text = (
                "Nos activités durent entre 30 minutes et 3 heures. Vous pouvez choisir selon votre disponibilité. "
                "Les activités courtes sont parfaites pour débuter !"
            )
        elif "rejoindre" in user_message or "participer" in user_message:
            response_text = (
                "Pour rejoindre La Vida Luca, rendez-vous sur la page 'Rejoindre' ou contactez-nous directement. "
                "Nous serons ravis de vous accueillir dans notre communauté !"
            )
        else:
            response_text = (
                "Je suis l'assistant IA de La Vida Luca ! Je peux vous aider avec les activités, "
                "la sécurité, et toutes vos questions sur notre projet. Que souhaitez-vous savoir ?"
            )
        
        context_used = message.context is not None
        
        response = ChatResponse(
            response=response_text,
            context_used=context_used
        )
        
        logger.info("Chat response generated successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors du traitement du message")

# Gestion des erreurs globales
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erreur interne du serveur"}
    )

# Point d'entrée pour Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=os.getenv("ENVIRONMENT") != "production"
    )