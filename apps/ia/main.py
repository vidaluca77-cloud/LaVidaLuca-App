"""
API FastAPI pour l'intelligence artificielle agricole de La Vida Luca.

Endpoints disponibles:
- /health : Vérification de la santé de l'API
- /guide : Guide et conseils agricoles personnalisés
- /chat : Chat interactif avec l'IA agricole
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv
import uvicorn

# Chargement des variables d'environnement
load_dotenv()

# Configuration
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", os.getenv("PORT", "8000")))
API_DEBUG = os.getenv("API_DEBUG", "false").lower() == "true"

# Initialisation de l'application FastAPI
app = FastAPI(
    title="La Vida Luca - API IA Agricole",
    description="API d'intelligence artificielle pour l'agriculture durable et l'accompagnement des jeunes en MFR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modèles Pydantic
class HealthResponse(BaseModel):
    status: str = "healthy"
    message: str = "API IA agricole opérationnelle"
    version: str = "1.0.0"

class GuideRequest(BaseModel):
    culture: str = Field(..., description="Type de culture (ex: tomates, légumes, céréales)")
    saison: str = Field(..., description="Saison actuelle (printemps, été, automne, hiver)")
    region: Optional[str] = Field(None, description="Région géographique")
    niveau: str = Field(default="débutant", description="Niveau d'expérience (débutant, intermédiaire, avancé)")

class GuideResponse(BaseModel):
    culture: str
    conseils: List[str]
    calendrier: List[str]
    ressources: List[str]
    niveau_difficulte: str

class ChatMessage(BaseModel):
    message: str = Field(..., description="Message de l'utilisateur")
    contexte: Optional[str] = Field(None, description="Contexte de la conversation")

class ChatResponse(BaseModel):
    reponse: str
    suggestions: List[str]
    ressources_utiles: List[str]

# Endpoints

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Vérification de la santé de l'API.
    Retourne le statut de l'API et des informations de base.
    """
    return HealthResponse()

@app.post("/guide", response_model=GuideResponse)
async def get_agricultural_guide(request: GuideRequest):
    """
    Génère un guide agricole personnalisé selon la culture et la saison.
    
    Fournit des conseils adaptés aux jeunes en formation agricole,
    avec un focus sur l'agriculture durable et les pratiques MFR.
    """
    
    # Simulation de conseils basés sur la culture et la saison
    conseils_base = {
        "tomates": {
            "printemps": [
                "Préparer les semis en intérieur dès mars",
                "Choisir des variétés adaptées à votre région",
                "Prévoir un système de tuteurage robuste"
            ],
            "été": [
                "Arroser régulièrement mais sans excès",
                "Tailler les gourmands pour favoriser la fructification",
                "Surveiller les maladies (mildiou, alternariose)"
            ],
            "automne": [
                "Récolter avant les premières gelées",
                "Conserver les graines des meilleures variétés",
                "Nettoyer et composter les plants"
            ],
            "hiver": [
                "Planifier les variétés pour la prochaine saison",
                "Préparer le sol pour les futures plantations",
                "Étudier les techniques de culture sous serre"
            ]
        },
        "légumes": {
            "printemps": [
                "Diversifier les cultures selon la rotation",
                "Commencer les semis de légumes de saison",
                "Préparer les parcelles avec compost"
            ],
            "été": [
                "Maintenir l'humidité du sol par paillage",
                "Récolter régulièrement pour stimuler la production",
                "Associer les cultures complémentaires"
            ],
            "automne": [
                "Semer les légumes d'hiver (mâche, épinards)",
                "Préparer les conserves et la transformation",
                "Couvrir le sol pour l'hiver"
            ],
            "hiver": [
                "Planifier les rotations de cultures",
                "Maintenir la production sous abris",
                "Former aux techniques de conservation"
            ]
        }
    }
    
    # Sélection des conseils appropriés
    culture_key = request.culture.lower()
    if culture_key not in conseils_base:
        culture_key = "légumes"  # Fallback par défaut
    
    conseils = conseils_base[culture_key].get(request.saison.lower(), conseils_base[culture_key]["printemps"])
    
    # Calendrier adapté à la saison
    calendrier = [
        f"Semaine 1-2: Préparation et planification",
        f"Semaine 3-4: Mise en œuvre des techniques de base",
        f"Semaine 5-8: Suivi et entretien régulier",
        f"Semaine 9-12: Récolte et évaluation"
    ]
    
    # Ressources pédagogiques MFR
    ressources = [
        "Guide technique MFR de l'agriculture durable",
        "Fiches pratiques La Vida Luca",
        "Réseau d'entraide entre apprenants",
        "Accompagnement par les maîtres de stage"
    ]
    
    return GuideResponse(
        culture=request.culture,
        conseils=conseils,
        calendrier=calendrier,
        ressources=ressources,
        niveau_difficulte=request.niveau
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """
    Chat interactif avec l'IA agricole de La Vida Luca.
    
    Répond aux questions des apprenants sur l'agriculture,
    l'insertion sociale et les techniques durables.
    """
    
    user_message = message.message.lower()
    
    # Système de réponses basé sur des mots-clés (simulation d'IA)
    responses = {
        "bonjour": {
            "reponse": "Bonjour ! Je suis l'assistant IA de La Vida Luca. Je suis là pour t'accompagner dans ton apprentissage agricole. Comment puis-je t'aider aujourd'hui ?",
            "suggestions": ["Demander des conseils de culture", "En savoir plus sur l'agriculture durable", "Découvrir les activités MFR"],
            "ressources": ["Guide du débutant", "Activités pratiques", "Réseau d'entraide"]
        },
        "culture": {
            "reponse": "L'agriculture durable est au cœur de notre approche à La Vida Luca. Nous privilégions les techniques respectueuses de l'environnement et adaptées aux jeunes en formation.",
            "suggestions": ["Techniques de permaculture", "Rotation des cultures", "Compostage et fertilisation naturelle"],
            "ressources": ["Fiches techniques", "Vidéos pédagogiques", "Retours d'expérience"]
        },
        "aide": {
            "reponse": "Je peux t'aider sur de nombreux sujets : techniques agricoles, conseils de saison, planification des cultures, ou questions sur l'insertion professionnelle en agriculture.",
            "suggestions": ["Poser une question spécifique", "Obtenir un guide de culture", "Découvrir les métiers agricoles"],
            "ressources": ["Base de connaissances", "Communauté d'apprenants", "Support technique"]
        }
    }
    
    # Détection du type de question
    response_key = "aide"  # Réponse par défaut
    for key in responses.keys():
        if key in user_message:
            response_key = key
            break
    
    response_data = responses[response_key]
    
    return ChatResponse(
        reponse=response_data["reponse"],
        suggestions=response_data["suggestions"],
        ressources_utiles=response_data["ressources"]
    )

@app.get("/")
async def root():
    """Page d'accueil de l'API."""
    return {
        "message": "Bienvenue sur l'API IA de La Vida Luca",
        "documentation": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_DEBUG
    )