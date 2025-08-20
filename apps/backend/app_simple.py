"""
Simple working FastAPI app for La Vida Luca.
This version bypasses the complex import structure for now.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging
import os
import uuid
from datetime import datetime

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


class AgriConsultationRequest(BaseModel):
    """Request model for agricultural consultation."""
    question: str
    context: Optional[str] = None
    category: Optional[str] = None


class AgriConsultationResponse(BaseModel):
    """Response model for agricultural consultation."""
    id: str
    question: str
    answer: str
    category: Optional[str] = None
    confidence_score: Optional[float] = None
    created_at: str
    session_id: Optional[str] = None


# Simple in-memory storage for consultations (for demo purposes)
consultations_storage = []


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


def get_agricultural_ai_response(question: str, context: Optional[str] = None) -> tuple[str, Optional[str], float]:
    """
    Get AI-powered agricultural consultation using OpenAI or fallback.
    Returns (answer, category, confidence_score).
    """
    try:
        # Try to use OpenAI if available
        import openai
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return get_fallback_agricultural_response(question, context)
        
        # Set up OpenAI client
        openai.api_key = api_key
        
        # Specialized agricultural system prompt
        system_prompt = """Vous êtes un expert agricole et en permaculture spécialisé dans l'aide aux jardiniers et agriculteurs français.
Votre expertise couvre le jardinage biologique, la santé des sols, la gestion naturelle des ravageurs, 
les rotations de cultures, l'irrigation et la planification saisonnière.

Donnez des conseils pratiques, basés sur des méthodes éprouvées et respectueuses de l'environnement.
Adaptez vos réponses au contexte français et aux pratiques de l'agriculture biologique.

Format de réponse attendu:
[Votre réponse détaillée ici]

Catégorie: [sol|plantes|ravageurs|irrigation|planification|general]
Confiance: [0.0-1.0]"""

        user_prompt = f"Question: {question}"
        if context:
            user_prompt += f"\nContexte: {context}"
        user_prompt += "\nVeuillez fournir des conseils détaillés et pratiques."

        # Call OpenAI API (using the older API format compatible with version 1.3.8)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        
        # Parse response to extract category and confidence
        lines = content.strip().split('\n')
        answer_lines = []
        category = None
        confidence = 0.8
        
        for line in lines:
            line = line.strip()
            if line.lower().startswith('catégorie:'):
                category = line.split(':', 1)[1].strip().lower()
            elif line.lower().startswith('confiance:'):
                try:
                    confidence = float(line.split(':', 1)[1].strip())
                except (ValueError, IndexError):
                    confidence = 0.8
            elif line and not line.lower().startswith(('catégorie:', 'confiance:')):
                answer_lines.append(line)
        
        answer = '\n'.join(answer_lines).strip()
        return answer, category, confidence
        
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        return get_fallback_agricultural_response(question, context)


def get_fallback_agricultural_response(question: str, context: Optional[str] = None) -> tuple[str, Optional[str], float]:
    """Fallback response when OpenAI is not available."""
    question_lower = question.lower()
    
    if any(word in question_lower for word in ['sol', 'terre', 'terreau', 'ph']):
        answer = """Pour améliorer votre sol, voici quelques conseils essentiels :

1. **Testez votre sol** : Connaître le pH et la composition vous aide à choisir les bonnes amendements.

2. **Ajoutez de la matière organique** : Compost, fumier décomposé, ou feuilles mortes enrichissent et structurent le sol.

3. **Évitez le travail du sol humide** : Cela peut créer des mottes compactes difficiles à corriger.

4. **Utilisez des couvre-sols** : Plantez des légumineuses ou gardez un paillis permanent.

5. **Rotation des cultures** : Alternez les familles de légumes pour préserver la fertilité.

Pour des conseils plus spécifiques, n'hésitez pas à préciser votre type de sol et votre région."""
        return answer, "sol", 0.9
    
    elif any(word in question_lower for word in ['compost', 'composte', 'décomposition']):
        answer = """Voici comment réussir votre compost :

1. **Équilibre vert/brun** : 1/3 de matières vertes (épluchures, tontes) pour 2/3 de matières brunes (feuilles sèches, carton).

2. **Humidité optimale** : Le compost doit être humide comme une éponge essorée.

3. **Aération régulière** : Retournez le tas toutes les 2-3 semaines pour apporter de l'oxygène.

4. **Taille des déchets** : Plus c'est petit, plus ça se décompose vite.

5. **Patience** : Comptez 6 à 12 mois selon les conditions et la méthode.

Un bon compost sent la terre de forêt et a une texture friable."""
        return answer, "sol", 0.9
    
    elif any(word in question_lower for word in ['ravageur', 'insecte', 'maladie', 'parasite', 'pucerons']):
        answer = """Pour gérer les ravageurs naturellement :

1. **Prévention** : Favorisez la biodiversité avec des plantes compagnes et des abris pour auxiliaires.

2. **Observation régulière** : Inspectez vos plantes pour détecter les problèmes tôt.

3. **Solutions douces** : Savon noir, huile de neem, ou purins de plantes (ortie, prêle).

4. **Auxiliaires naturels** : Encouragez coccinelles, oiseaux, et autres prédateurs naturels.

5. **Rotation et hygiène** : Nettoyez les débris végétaux et alternez les cultures.

Précisez quel ravageur vous préoccupe pour des conseils plus ciblés."""
        return answer, "ravageurs", 0.9
    
    elif any(word in question_lower for word in ['arrosage', 'irrigation', 'eau', 'sécheresse']):
        answer = """Conseils pour un arrosage efficace :

1. **Arrosez le matin** : Moins d'évaporation et les plantes ont le temps de sécher avant la nuit.

2. **Au pied des plantes** : Évitez les feuilles pour réduire les maladies.

3. **Abondamment mais moins souvent** : Encouragez les racines profondes.

4. **Paillez** : Gardez l'humidité et réduisez l'évaporation.

5. **Récupérez l'eau de pluie** : Écologique et économique.

Adaptez la fréquence selon votre type de sol et les conditions météo."""
        return answer, "irrigation", 0.9
    
    elif any(word in question_lower for word in ['plantation', 'semer', 'planter', 'calendrier', 'quand']):
        answer = """Guide pour bien planifier vos plantations :

1. **Connaissez votre zone climatique** : Respectez les dernières gelées de votre région.

2. **Calendrier lunaire** : Optionnel mais apprécié par beaucoup de jardiniers.

3. **Rotation des cultures** : Évitez de planter la même famille au même endroit.

4. **Associations bénéfiques** : Basilic avec tomates, radis avec carottes, etc.

5. **Échelonnez les semis** : Pour avoir des récoltes étalées dans le temps.

Précisez quels légumes vous voulez cultiver pour des conseils plus spécifiques."""
        return answer, "planification", 0.9
    
    else:
        answer = f"""Merci pour votre question sur l'agriculture : "{question}"

Je suis votre assistant agricole IA spécialisé dans :
- Le jardinage biologique et la permaculture
- La santé des sols et le compostage  
- La gestion naturelle des ravageurs
- La planification des cultures et rotations
- L'irrigation et l'économie d'eau
- Les techniques agricoles durables

Pouvez-vous préciser votre domaine d'intérêt pour que je puisse vous donner des conseils plus adaptés ?

N'hésitez pas à mentionner votre région et votre niveau d'expérience pour des recommandations personnalisées."""
        return answer, "general", 0.7


@app.post("/api/v1/agri-assistant", response_model=AgriConsultationResponse)
async def create_agri_consultation(request: AgriConsultationRequest):
    """
    Create a new agricultural consultation with AI assistance.
    """
    try:
        # Get AI response
        answer, category, confidence = get_agricultural_ai_response(
            question=request.question,
            context=request.context
        )
        
        # Create consultation record
        consultation_id = str(uuid.uuid4())
        created_at = datetime.utcnow().isoformat()
        
        consultation = {
            "id": consultation_id,
            "question": request.question,
            "answer": answer,
            "category": category or request.category,
            "confidence_score": confidence,
            "created_at": created_at,
            "session_id": getattr(request, 'session_id', None)
        }
        
        # Store in memory (in a real app, this would be in database)
        consultations_storage.append(consultation)
        
        # Keep only last 100 consultations to avoid memory issues
        if len(consultations_storage) > 100:
            consultations_storage.pop(0)
        
        return AgriConsultationResponse(**consultation)
        
    except Exception as e:
        logger.error(f"Error in agricultural consultation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors du traitement de votre consultation agricole"
        )


@app.get("/api/v1/agri-assistant/history")
async def get_agri_consultation_history(
    limit: int = 10,
    category: Optional[str] = None
):
    """
    Get recent agricultural consultations history.
    """
    try:
        # Filter by category if specified
        filtered_consultations = consultations_storage
        if category:
            filtered_consultations = [
                c for c in consultations_storage 
                if c.get("category") == category
            ]
        
        # Sort by creation date (newest first) and limit
        sorted_consultations = sorted(
            filtered_consultations,
            key=lambda x: x["created_at"],
            reverse=True
        )[:limit]
        
        return {
            "consultations": sorted_consultations,
            "total_count": len(filtered_consultations),
            "showing": len(sorted_consultations)
        }
        
    except Exception as e:
        logger.error(f"Error getting consultation history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la récupération de l'historique"
        )


@app.get("/api/v1/agri-assistant/health")
async def agri_assistant_health():
    """Health check for agricultural assistant service."""
    return {
        "status": "healthy",
        "service": "agricultural_assistant",
        "ai_enabled": os.getenv("OPENAI_API_KEY") is not None,
        "model": "gpt-3.5-turbo",
        "consultations_stored": len(consultations_storage)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)