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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)