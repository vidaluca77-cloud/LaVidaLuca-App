"""
Guide endpoint for AI-powered assistance with robust OpenAI client initialization.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
import logging
import os
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

class GuideRequest(BaseModel):
    """Request model for guide endpoint."""
    question: str
    context: Optional[str] = None

class GuideResponse(BaseModel):
    """Response model for guide endpoint."""
    answer: str
    confidence: Optional[float] = None
    sources: Optional[list[str]] = None

def get_openai_client():
    """Initialize OpenAI client at call time with error handling."""
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service unavailable: API key not configured"
        )
    
    try:
        # Import OpenAI only when needed to avoid boot crashes
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except ImportError:
        logger.error("OpenAI package not installed")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service unavailable: package not installed"
        )
    except Exception as e:
        logger.error(f"Failed to initialize OpenAI client: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OpenAI service unavailable: initialization failed"
        )

@router.post("/guide", response_model=GuideResponse)
async def get_guide(request: GuideRequest):
    """
    Get AI-powered guidance for questions about sustainable living and gardening.
    
    This endpoint provides helpful advice and guidance for questions related to:
    - Sustainable living practices
    - Gardening and permaculture
    - Local community activities
    - Environmental conservation
    """
    try:
        # Initialize OpenAI client at call time
        client = get_openai_client()
        
        # Prepare the system prompt
        system_prompt = """
You are an expert guide for sustainable living, gardening, and permaculture practices. 
Provide helpful, practical advice in French for questions about:
- Sustainable living and ecological practices
- Gardening, permaculture, and soil management
- Local community initiatives and rural development
- Environmental conservation and biodiversity

Respond in a friendly, informative manner with specific, actionable advice.
"""
        
        # Make OpenAI API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.question}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        answer = response.choices[0].message.content
        
        return GuideResponse(
            answer=answer,
            confidence=0.8,
            sources=["OpenAI GPT-3.5-turbo", "La Vida Luca AI Assistant"]
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions (like 503 from get_openai_client)
        raise
    except Exception as e:
        logger.error(f"Error in guide endpoint: {str(e)}")
        # Fall back to basic response if OpenAI fails
        fallback_answer = f"""
Merci pour votre question : \"{request.question}\"

Je rencontre actuellement des difficultés techniques avec le service IA. 
En attendant, voici quelques conseils généraux :

Pour le jardinage et la permaculture :
• Connaître son sol (pH, composition)
• Choisir des plantes adaptées au climat local
• Pratiquer la rotation des cultures
• Utiliser le compost et la matière organique
• Préserver la biodiversité

Pour la vie durable :
• Réduire, réutiliser, recycler
• Privilégier les circuits courts
• Économiser l'eau et l'énergie
• Favoriser les transports doux

N'hésitez pas à reposer votre question plus tard !
"""
        
        return GuideResponse(
            answer=fallback_answer,
            confidence=0.3,
            sources=["La Vida Luca Fallback System"]
        )

@router.get("/guide/health")
async def guide_health():
    """Health check for guide service without external dependencies."""
    api_key_configured = bool(os.environ.get('OPENAI_API_KEY'))
    
    return {
        "status": "healthy",
        "service": "guide",
        "timestamp": "2025-09-04T20:32:00Z",
        "api_key_configured": api_key_configured,
        "openai_available": api_key_configured
    }

@router.get("/health")
async def health():
    """General health check endpoint that returns 200 without external dependencies."""
    return {
        "status": "healthy",
        "service": "lavidaluca-backend",
        "timestamp": "2025-09-04T20:32:00Z",
        "components": {
            "database": "not_checked",
            "openai": "conditional",
            "guide_service": "healthy"
        }
    }
