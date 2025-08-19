from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
import json

# Charger les variables d'environnement
load_dotenv()

# Configuration
app = FastAPI(
    title="La Vida Luca IA API",
    description="API IA pour le projet La Vida Luca - Formation et agriculture durable",
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
class GuideRequest(BaseModel):
    activite_id: str
    profil_utilisateur: Optional[dict] = None
    contexte: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    contexte: Optional[str] = None
    historique: Optional[List[dict]] = None

class GuideResponse(BaseModel):
    activite: str
    conseils: List[str]
    materiel_necessaire: List[str]
    etapes: List[str]
    conseils_securite: List[str]
    adapte_au_profil: bool

class ChatResponse(BaseModel):
    reponse: str
    suggestions: Optional[List[str]] = None
    ressources: Optional[List[str]] = None

# Base de données simulée des activités
ACTIVITES_DB = {
    "semis-plantation": {
        "title": "Semis & plantation",
        "category": "agri",
        "conseils": [
            "Respecter les périodes de semis selon les variétés",
            "Préparer le sol en amont (bêchage, amendement)",
            "Adapter la profondeur de plantation"
        ],
        "materiel": ["bêche", "serfouette", "arrosoir", "graines", "paillis"],
        "etapes": [
            "Préparer le terrain (désherbage, ameublissement)",
            "Tracer les sillons à la profondeur appropriée",
            "Semer en respectant les distances",
            "Recouvrir légèrement et tasser",
            "Arroser en pluie fine",
            "Protéger si nécessaire (voile, cloches)"
        ],
        "securite": [
            "Porter des gants pour manipuler la terre",
            "Attention aux outils tranchants",
            "S'hydrater régulièrement"
        ]
    },
    "elevage-soins": {
        "title": "Soins aux animaux d'élevage",
        "category": "agri",
        "conseils": [
            "Observer quotidiennement le comportement des animaux",
            "Maintenir la propreté des espaces de vie",
            "Respecter les horaires d'alimentation"
        ],
        "materiel": ["bottes", "gants", "nourriture adaptée", "matériel de nettoyage"],
        "etapes": [
            "Vérifier l'état général des animaux",
            "Nettoyer les abreuvoirs et mangeoires",
            "Distribuer la nourriture adaptée",
            "Nettoyer les espaces de vie",
            "Noter toute observation particulière"
        ],
        "securite": [
            "Approcher les animaux calmement",
            "Porter des équipements de protection",
            "Connaître les gestes d'urgence"
        ]
    }
}

# Routes API

@app.get("/health")
async def health_check():
    """Point de contrôle de santé de l'API"""
    return {
        "status": "healthy",
        "service": "La Vida Luca IA API",
        "version": "1.0.0"
    }

@app.post("/guide", response_model=GuideResponse)
async def get_activity_guide(request: GuideRequest):
    """
    Génère un guide personnalisé pour une activité donnée
    """
    activite_id = request.activite_id
    
    # Vérifier si l'activité existe
    if activite_id not in ACTIVITES_DB:
        raise HTTPException(status_code=404, detail="Activité non trouvée")
    
    activite = ACTIVITES_DB[activite_id]
    
    # Adaptation basique au profil utilisateur
    adapte_au_profil = True
    if request.profil_utilisateur:
        # Logique d'adaptation simple (peut être étendue)
        niveau = request.profil_utilisateur.get("niveau", "debutant")
        if niveau == "debutant":
            # Ajouter des conseils supplémentaires pour débutants
            conseils_adaptes = activite["conseils"] + [
                "Demander l'aide d'un encadrant si c'est votre première fois",
                "Commencer par observer avant de pratiquer"
            ]
        else:
            conseils_adaptes = activite["conseils"]
    else:
        conseils_adaptes = activite["conseils"]
    
    return GuideResponse(
        activite=activite["title"],
        conseils=conseils_adaptes,
        materiel_necessaire=activite["materiel"],
        etapes=activite["etapes"],
        conseils_securite=activite["securite"],
        adapte_au_profil=adapte_au_profil
    )

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """
    Interface de chat avec l'IA pour répondre aux questions
    """
    user_message = message.message.lower()
    
    # Réponses simulées basées sur des mots-clés
    if "activité" in user_message or "que faire" in user_message:
        reponse = """Je peux t'aider à choisir une activité ! 🌱
        
Voici quelques suggestions selon tes intérêts :
- **Agriculture** : semis, plantation, soins aux animaux
- **Transformation** : fromage, conserves, pain
- **Artisanat** : menuiserie, construction, réparation
- **Environnement** : plantation, compostage, écologie
- **Animation** : accueil, visites, ateliers

Dis-moi ce qui t'intéresse le plus !"""
        
        suggestions = [
            "Montre-moi les activités agricoles",
            "Je veux apprendre l'artisanat",
            "Quelles activités pour débutants ?"
        ]
    
    elif "sécurité" in user_message or "protection" in user_message:
        reponse = """La sécurité est primordiale dans toutes nos activités ! 🛡️

Règles générales :
- Toujours porter les équipements de protection appropriés
- Suivre les consignes de l'encadrant
- Signaler tout incident ou matériel défaillant
- S'hydrater régulièrement
- Respecter son niveau et ses limites

Chaque activité a ses spécificités de sécurité."""
        
        suggestions = [
            "Équipements pour les activités agricoles",
            "Sécurité en atelier menuiserie",
            "Que faire en cas d'accident ?"
        ]
    
    elif "materiel" in user_message or "équipement" in user_message:
        reponse = """Chaque activité nécessite du matériel spécifique 🔧

Matériel de base souvent utilisé :
- **Vêtements** : bottes, gants, tablier, vêtements de travail
- **Outils agricoles** : bêche, serfouette, arrosoir, sécateur
- **Protection** : lunettes, casque, gants renforcés
- **Hygiène** : savon, désinfectant, trousse de premiers secours

Le matériel est fourni, mais tu peux apporter tes affaires personnelles."""
        
        suggestions = [
            "Matériel pour l'activité semis",
            "Protection pour l'élevage",
            "Outils de menuiserie disponibles"
        ]
    
    else:
        reponse = """Bonjour ! Je suis l'assistant IA de La Vida Luca 🌾

Je peux t'aider avec :
- **Choix d'activités** selon tes intérêts et niveau
- **Guides pratiques** pour chaque activité
- **Conseils de sécurité** et bonnes pratiques
- **Information sur le matériel** nécessaire
- **Questions générales** sur le projet

Que veux-tu savoir ?"""
        
        suggestions = [
            "Quelles activités puis-je faire ?",
            "Comment bien débuter ?",
            "Règles de sécurité importantes"
        ]
    
    return ChatResponse(
        reponse=reponse,
        suggestions=suggestions,
        ressources=[
            "Guide des activités La Vida Luca",
            "Règles de sécurité",
            "Catalogue du matériel"
        ]
    )

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API IA de La Vida Luca !",
        "documentation": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )