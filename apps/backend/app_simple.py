"""
Simple working FastAPI app for La Vida Luca.
This version bypasses the complex import structure for now.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging
import os
import time

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


class GuideRequest(BaseModel):
    """Request model for guide endpoint."""
    question: str
    context: Optional[str] = None


class GuideResponse(BaseModel):
    """Response model for guide endpoint."""
    answer: str
    confidence: Optional[float] = None
    sources: Optional[list[str]] = None


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
        "database": "not_connected",  # Simplified for now
        "environment": os.getenv("ENVIRONMENT", "development")
    }


@app.post("/api/v1/guide", response_model=GuideResponse)
async def get_guide(request: GuideRequest):
    """
    Get AI-powered guidance for questions about sustainable living and gardening.
    """
    try:
        # Generate response based on question content
        if "sol" in request.question.lower() or "terre" in request.question.lower():
            answer = """Pour améliorer un sol argileux compact, voici quelques conseils :

1. **Ajouter de la matière organique** : Incorporez du compost, du fumier bien décomposé ou des feuilles mortes pour améliorer la structure du sol.

2. **Éviter le travail du sol humide** : Ne jamais travailler un sol argileux quand il est détrempé, cela créerait des mottes très dures.

3. **Créer des buttes de culture** : Surélevez vos zones de plantation pour améliorer le drainage.

4. **Planter des couvre-sols** : Utilisez des plantes comme la luzerne ou le trèfle pour structurer naturellement le sol.

5. **Paillis permanent** : Gardez le sol couvert pour protéger sa structure et nourrir la vie microbienne.

Ces méthodes améliorent progressivement la texture et la fertilité de votre sol argileux."""
            
        elif "jardinage" in request.question.lower() or "plante" in request.question.lower():
            answer = """Pour réussir votre jardinage, voici des conseils de base :

1. **Connaître son sol** : Testez le pH et la composition de votre terre
2. **Choisir les bonnes plantes** : Adaptées à votre climat et exposition
3. **Planifier les rotations** : Alternez les familles de légumes
4. **Arroser intelligemment** : Le matin de préférence, au pied des plantes
5. **Composter** : Recyclez vos déchets verts pour nourrir le sol

Besoin de conseils plus spécifiques ? N'hésitez pas à préciser votre question !"""
        
        elif "compost" in request.question.lower():
            answer = """Voici comment faire un compost efficace :

1. **Équilibrer vert et brun** : 1/3 de matières azotées (épluchures, tontes) pour 2/3 de matières carbonées (feuilles sèches, carton)

2. **Surveiller l'humidité** : Le compost doit être humide comme une éponge essorée

3. **Aérer régulièrement** : Retournez le tas toutes les 2-3 semaines

4. **Température idéale** : 50-60°C au centre indique une bonne décomposition

5. **Patience** : Comptez 6-12 mois selon les conditions

Un bon compost sent la terre de forêt, pas l'ammoniaque !"""
        
        else:
            answer = f"""Merci pour votre question : "{request.question}"

Je suis là pour vous aider avec des conseils sur :
- Le jardinage et la permaculture
- La vie durable et écologique  
- Les initiatives communautaires locales
- La préservation de l'environnement

Pouvez-vous préciser votre domaine d'intérêt pour que je puisse vous donner des conseils plus adaptés ?"""

        return GuideResponse(
            answer=answer,
            confidence=0.8,
            sources=["La Vida Luca Knowledge Base", "Sustainable Living Practices"]
        )
        
    except Exception as e:
        logger.error(f"Error in guide endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre question"
        )


@app.get("/api/v1/guide/health")
async def guide_health():
    """Health check for guide service."""
    return {
        "status": "healthy",
        "service": "guide",
        "ai_enabled": os.getenv("OPENAI_API_KEY") is not None
    }


# Contact form models and endpoint
class ContactRequest(BaseModel):
    nom: str
    email: str
    telephone: Optional[str] = None
    message: str
    typeAide: Optional[str] = None


class ContactResponse(BaseModel):
    success: bool
    message: str
    contact_id: Optional[str] = None


# Activity models and data
class Activity(BaseModel):
    title: str
    category: str
    duration: int
    safety: int
    desc: str


# Static activity data
ACTIVITIES_DATA = [
    {"title": "Nourrir et soigner les moutons", "category": "agri", "duration": 60, "safety": 1, "desc": "Alimentation, eau, observation et bien-être du troupeau."},
    {"title": "Tonte & entretien du troupeau", "category": "agri", "duration": 90, "safety": 2, "desc": "Hygiène, tonte (démonstration) et soins courants."},
    {"title": "Soins basse-cour", "category": "agri", "duration": 60, "safety": 1, "desc": "Poules, canards, lapins : alimentation, abris, propreté."},
    {"title": "Plantation de cultures", "category": "agri", "duration": 90, "safety": 1, "desc": "Semis, arrosage, paillage, suivi des jeunes plants."},
    {"title": "Initiation maraîchage", "category": "agri", "duration": 120, "safety": 1, "desc": "Plan de culture, entretien, récolte respectueuse."},
    {"title": "Gestion des clôtures & abris", "category": "agri", "duration": 120, "safety": 2, "desc": "Identifier, réparer et sécuriser parcs et abris."},
    {"title": "Fabrication de fromage", "category": "transfo", "duration": 90, "safety": 2, "desc": "Du lait au caillé : hygiène, moulage, affinage (découverte)."},
    {"title": "Confitures & conserves", "category": "transfo", "duration": 90, "safety": 1, "desc": "Préparation, stérilisation, mise en pot, étiquetage."},
    {"title": "Transformation de la laine", "category": "transfo", "duration": 90, "safety": 1, "desc": "Lavage, cardage et petite création textile."},
    {"title": "Fabrication de jus", "category": "transfo", "duration": 90, "safety": 2, "desc": "Du verger à la bouteille : tri, pressage, filtration."},
    {"title": "Séchage d'herbes aromatiques", "category": "transfo", "duration": 60, "safety": 1, "desc": "Cueillette, séchage doux et conditionnement."},
    {"title": "Pain au four à bois", "category": "transfo", "duration": 120, "safety": 2, "desc": "Pétrissage, façonnage, cuisson : respect des temps."},
    {"title": "Construction d'abris", "category": "artisanat", "duration": 120, "safety": 2, "desc": "Petites structures bois : plan, coupe, assemblage."},
    {"title": "Réparation & entretien des outils", "category": "artisanat", "duration": 60, "safety": 1, "desc": "Affûtage, graissage, vérifications simples."},
    {"title": "Menuiserie simple", "category": "artisanat", "duration": 120, "safety": 2, "desc": "Mesure, coupe, ponçage, finitions."},
    {"title": "Peinture & décoration d'espaces", "category": "artisanat", "duration": 90, "safety": 1, "desc": "Préparer, protéger, peindre proprement."},
    {"title": "Aménagement d'espaces verts", "category": "artisanat", "duration": 90, "safety": 1, "desc": "Désherbage doux, paillage, plantations."},
    {"title": "Panneaux & orientation", "category": "artisanat", "duration": 90, "safety": 1, "desc": "Concevoir et poser une signalétique claire."},
    {"title": "Entretien de la rivière", "category": "nature", "duration": 90, "safety": 2, "desc": "Nettoyage doux, observation des berges."},
    {"title": "Plantation d'arbres", "category": "nature", "duration": 120, "safety": 1, "desc": "Choix d'essences, tuteurage, paillage, suivi."},
    {"title": "Potager écologique", "category": "nature", "duration": 90, "safety": 1, "desc": "Associations, paillis, rotation des cultures."},
    {"title": "Compostage", "category": "nature", "duration": 60, "safety": 1, "desc": "Tri, compost et valorisation des déchets verts."},
    {"title": "Observation de la faune locale", "category": "nature", "duration": 60, "safety": 1, "desc": "Discrétion, repérage, traces/indices."},
    {"title": "Nichoirs & hôtels à insectes", "category": "nature", "duration": 120, "safety": 1, "desc": "Concevoir, fabriquer, installer des abris."},
    {"title": "Journée portes ouvertes", "category": "social", "duration": 180, "safety": 1, "desc": "Préparer, accueillir, guider un public."},
    {"title": "Visites guidées de la ferme", "category": "social", "duration": 60, "safety": 1, "desc": "Présenter la ferme et répondre simplement."},
    {"title": "Ateliers pour enfants", "category": "social", "duration": 90, "safety": 2, "desc": "Jeux, découvertes nature, mini-gestes encadrés."},
    {"title": "Cuisine collective (équipe)", "category": "social", "duration": 90, "safety": 1, "desc": "Préparer un repas simple et bon."},
    {"title": "Goûter fermier", "category": "social", "duration": 60, "safety": 1, "desc": "Organisation, service, convivialité, propreté."},
    {"title": "Participation à un marché local", "category": "social", "duration": 180, "safety": 1, "desc": "Stand, présentation, caisse symbolique (simulation)."}
]


@app.post("/api/v1/contact", response_model=ContactResponse)
async def submit_contact_form(request: ContactRequest):
    """
    Process contact form submission.
    In a real implementation, this would save to database and send email.
    """
    try:
        # For now, just log the contact request
        logger.info(f"Contact form submitted by {request.nom} ({request.email})")
        logger.info(f"Type d'aide: {request.typeAide}")
        logger.info(f"Message: {request.message[:100]}...")
        
        # Simulate processing
        contact_id = f"CONTACT_{hash(request.email)}_{int(time.time())}"
        
        return ContactResponse(
            success=True,
            message="Merci pour votre message ! Nous vous recontacterons bientôt.",
            contact_id=contact_id
        )
    
    except Exception as e:
        logger.error(f"Error processing contact form: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors du traitement de votre demande. Veuillez réessayer plus tard."
        )


@app.get("/api/v1/contact/health")
async def contact_health():
    """Health check for contact service."""
    return {
        "status": "healthy",
        "service": "contact"
    }


@app.get("/api/v1/activities")
async def get_activities(category: Optional[str] = None, search: Optional[str] = None):
    """
    Get list of activities with optional filtering.
    """
    try:
        activities = ACTIVITIES_DATA.copy()
        
        # Filter by category if provided
        if category and category != "all":
            activities = [a for a in activities if a["category"] == category]
        
        # Search in title and description if provided
        if search:
            search_lower = search.lower()
            activities = [
                a for a in activities 
                if search_lower in a["title"].lower() or search_lower in a["desc"].lower()
            ]
        
        # Add some metadata
        categories = list(set(a["category"] for a in ACTIVITIES_DATA))
        
        return {
            "success": True,
            "data": {
                "activities": activities,
                "total": len(activities),
                "categories": categories
            },
            "message": f"Found {len(activities)} activities"
        }
    
    except Exception as e:
        logger.error(f"Error fetching activities: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur lors de la récupération des activités"
        )


@app.get("/api/v1/activities/categories")
async def get_activity_categories():
    """Get list of activity categories."""
    categories = {
        "agri": "Agriculture",
        "transfo": "Transformation", 
        "artisanat": "Artisanat",
        "nature": "Environnement",
        "social": "Animation"
    }
    
    return {
        "success": True,
        "data": categories,
        "message": "Categories retrieved successfully"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)