"""
Minimal backend with agricultural assistant for testing.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="La Vida Luca API",
    description="API pour la plateforme collaborative La Vida Luca",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Agricultural Assistant Models
class ConsultationCreate(BaseModel):
    question: str
    category: Optional[str] = None
    session_id: Optional[str] = None


class ConsultationResponse(BaseModel):
    response: str


class Consultation(BaseModel):
    id: int
    question: str
    response: str
    category: Optional[str] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    created_at: str


class Category(BaseModel):
    value: str
    label: str


# In-memory storage for demo
consultations_db = []
next_id = 1


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to La Vida Luca API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "in_memory",
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.post("/api/v1/agri-assistant/ask", response_model=ConsultationResponse)
async def ask_agricultural_assistant(consultation_data: ConsultationCreate):
    """
    Ask the agricultural AI assistant a question.
    """
    global next_id
    
    try:
        # Mock agricultural responses based on category and keywords
        question = consultation_data.question.lower()
        
        if consultation_data.category == "agriculture" or "culture" in question or "plantation" in question:
            response = """**Conseils pour vos cultures :**

1. **Préparation du sol** : Testez le pH (idéal entre 6.0-7.0) et enrichissez avec du compost
2. **Rotation des cultures** : Alternez légumineuses, légumes-feuilles et légumes-racines
3. **Calendrier de plantation** : Respectez les périodes selon votre région
4. **Arrosage** : Privilégiez un arrosage abondant mais moins fréquent
5. **Observation** : Surveillez régulièrement vos plants pour détecter maladies et ravageurs

Pour des conseils plus spécifiques, précisez votre type de culture et votre région."""
            
        elif consultation_data.category == "elevage" or "élevage" in question or "animal" in question:
            response = """**Conseils pour l'élevage :**

1. **Bien-être animal** : Assurez un logement adapté, propre et spacieux
2. **Alimentation** : Équilibrez les rations selon les besoins nutritionnels
3. **Santé préventive** : Respectez le calendrier de vaccination et vermifugation
4. **Gestion du pâturage** : Pratiquez la rotation pour préserver les prairies
5. **Réglementation** : Tenez à jour les registres d'élevage obligatoires

Précisez votre type d'élevage pour des conseils adaptés !"""
            
        elif consultation_data.category == "jardinage" or "jardin" in question or "potager" in question:
            response = """**Conseils pour votre jardin :**

1. **Planification** : Dessinez votre jardin en tenant compte de l'exposition
2. **Sol vivant** : Nourrissez-le avec compost et paillis organiques
3. **Biodiversité** : Mélangez légumes, aromates et fleurs compagnes
4. **Économie d'eau** : Paillez et récupérez l'eau de pluie
5. **Outils** : Entretenez vos outils pour un travail efficace

Un jardin productif demande patience et observation. Que voulez-vous cultiver ?"""
            
        elif consultation_data.category == "sols" or "sol" in question or "terre" in question:
            response = """**Gestion des sols :**

1. **Analyse** : Testez pH, matière organique et structure
2. **Amendements** : Ajoutez compost, fumier ou chaux selon les besoins
3. **Couverture** : Gardez le sol couvert (paillis, engrais verts)
4. **Aération** : Évitez le tassement, utilisez grelinette ou fourche-bêche
5. **Vie du sol** : Favorisez vers de terre et micro-organismes

Un sol sain est la base de toute agriculture productive. Quel est votre type de sol ?"""
            
        elif consultation_data.category == "maladies" or "maladie" in question or "ravageur" in question:
            response = """**Prévention et traitement :**

1. **Prévention** : Rotation des cultures, variétés résistantes, espacement adéquat
2. **Observation** : Inspection régulière des plants (dessous des feuilles)
3. **Biodiversité** : Favorisez auxiliaires avec haies et plantes mellifères
4. **Traitements bio** : Purin d'ortie, savon noir, bacille de Thuringe
5. **Intervention rapide** : Isolez plants malades, éliminez parties atteintes

Décrivez les symptômes observés pour un diagnostic précis !"""
            
        elif consultation_data.category == "irrigation" or "eau" in question or "arrosage" in question:
            response = """**Gestion de l'eau :**

1. **Récupération** : Installez récupérateurs d'eau de pluie
2. **Paillage** : Réduisez l'évaporation avec paillis organiques
3. **Goutte-à-goutte** : Économisez l'eau avec arrosage localisé
4. **Horaires** : Arrosez tôt le matin ou en soirée
5. **Plantes adaptées** : Choisissez variétés résistantes à la sécheresse

L'eau est précieuse : optimisez chaque goutte ! Quel est votre système actuel ?"""
            
        elif consultation_data.category == "bio" or "biologique" in question or "bio" in question:
            response = """**Agriculture biologique :**

1. **Certification** : Respectez cahier des charges et contrôles annuels
2. **Fertilisation** : Compost, fumier, engrais verts uniquement
3. **Protection** : Méthodes préventives et produits autorisés
4. **Semences** : Privilégiez semences bio et variétés anciennes
5. **Biodiversité** : Créez habitats pour auxiliaires naturels

Le bio, c'est un système global. Où en êtes-vous dans votre conversion ?"""
            
        elif consultation_data.category == "reglementation" or "réglementation" in question or "administration" in question:
            response = """**Réglementation agricole :**

1. **Déclarations** : MSA, PAC, registres d'exploitation
2. **Normes** : Bien-être animal, environnement, sécurité alimentaire
3. **Aides** : DJA, ICHN, MAE selon votre situation
4. **Formation** : Certiphyto obligatoire pour produits phytosanitaires
5. **Contrôles** : Tenez documents à jour (traçabilité, factures)

La réglementation évolue : restez informé ! Quel aspect vous préoccupe ?"""
            
        else:
            response = f"""**Bonjour ! Je suis votre assistant agricole spécialisé.**

Vous avez posé cette question : "{consultation_data.question}"

Je peux vous aider sur :
🌱 **Agriculture et cultures** - Techniques, rotations, fertilisation
🐄 **Élevage** - Bien-être animal, alimentation, gestion du troupeau  
🌿 **Jardinage** - Potager, permaculture, biodiversité
🌍 **Sols** - Analyse, amendements, vie du sol
🔬 **Maladies et ravageurs** - Prévention, diagnostic, traitements bio
💧 **Irrigation** - Économie d'eau, systèmes d'arrosage
🌿 **Agriculture biologique** - Conversion, certification, pratiques
📋 **Réglementation** - Normes, déclarations, aides

Pour des conseils plus précis, n'hésitez pas à reformuler votre question en précisant votre situation !"""

        # Save consultation to mock database
        consultation = Consultation(
            id=next_id,
            question=consultation_data.question,
            response=response,
            category=consultation_data.category,
            session_id=consultation_data.session_id,
            created_at="2025-08-20T00:00:00Z"
        )
        consultations_db.append(consultation)
        next_id += 1
        
        return ConsultationResponse(response=response)
        
    except Exception as e:
        logger.error(f"Error in agricultural consultation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la consultation agricole"
        )


@app.get("/api/v1/agri-assistant/history", response_model=List[Consultation])
async def get_consultation_history(
    skip: int = 0,
    limit: int = 20,
    session_id: Optional[str] = None
):
    """
    Get consultation history by session ID.
    """
    if session_id:
        filtered = [c for c in consultations_db if c.session_id == session_id]
    else:
        filtered = consultations_db
    
    return filtered[skip:skip + limit]


@app.get("/api/v1/agri-assistant/categories")
async def get_consultation_categories():
    """
    Get available consultation categories.
    """
    return {
        "categories": [
            {"value": "agriculture", "label": "Agriculture générale"},
            {"value": "elevage", "label": "Élevage"},
            {"value": "jardinage", "label": "Jardinage"},
            {"value": "sols", "label": "Gestion des sols"},
            {"value": "maladies", "label": "Maladies et ravageurs"},
            {"value": "irrigation", "label": "Irrigation et eau"},
            {"value": "bio", "label": "Agriculture biologique"},
            {"value": "reglementation", "label": "Réglementation"},
        ]
    }


@app.delete("/api/v1/agri-assistant/{consultation_id}")
async def delete_consultation(consultation_id: int):
    """
    Delete a consultation from history.
    """
    global consultations_db
    consultations_db = [c for c in consultations_db if c.id != consultation_id]
    return {"message": "Consultation deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)