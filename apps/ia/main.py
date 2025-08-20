"""
La Vida Luca IA Service - OpenAI Integration
Provides AI-powered suggestions and guidance for the MFR platform
"""

import os
import logging
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import structlog

# Load environment variables
load_dotenv()

# Configure structured logging
logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()

# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting La Vida Luca IA Service")
    yield
    logger.info("Shutting down La Vida Luca IA Service")

app = FastAPI(
    title="La Vida Luca IA Service",
    description="AI-powered guidance and suggestions for MFR training platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "https://lavidaluca.vercel.app",
        "https://lavidaluca-backend.render.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class GuideReq(BaseModel):
    question: str

class GuideRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500, description="User's question")
    context: Optional[str] = Field(None, max_length=1000, description="Additional context")
    user_level: Optional[str] = Field("beginner", description="User's experience level")

class GuideResponse(BaseModel):
    title: str
    answer: str
    question_echo: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: list[str] = []

class SuggestionRequest(BaseModel):
    user_profile: str = Field(..., description="User's interests and background")
    category: Optional[str] = Field(None, description="Specific category of interest")
    difficulty: Optional[str] = Field("all", description="Preferred difficulty level")

class SuggestionResponse(BaseModel):
    suggestions: list[dict]
    reasoning: str

# Health check
@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "IA Service",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY"))
    }

# Legacy endpoint for compatibility
@app.post("/guide")
def guide(req: GuideReq):
    """Legacy guide endpoint for backward compatibility"""
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        return {
            "title": "Conseil IA",
            "answer": "L'IA n'est pas encore configurée. Contactez l'administrateur pour activer les conseils personnalisés.",
            "question_echo": req.question
        }
    
    # Return enhanced response
    return {
        "title": "Conseil Personnalisé",
        "answer": f"Voici mon conseil concernant '{req.question}': basez-vous sur les bonnes pratiques agricoles et n'hésitez pas à consulter vos formateurs pour des conseils spécifiques à votre région et votre filière.",
        "question_echo": req.question
    }

# AI Guide endpoint
@app.post("/api/v1/guide", response_model=GuideResponse)
async def get_guidance(request: GuideRequest):
    """Get AI-powered guidance for user questions"""
    logger.info("Guidance request received", question=request.question)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_key:
        logger.warning("OpenAI API key not configured")
        return GuideResponse(
            title="Configuration Notice",
            answer="L'IA n'est pas encore configurée. Veuillez contacter l'administrateur pour activer les conseils personnalisés.",
            question_echo=request.question,
            confidence=0.0
        )
    
    try:
        # For now, return a structured mock response
        return GuideResponse(
            title="Conseil Personnalisé",
            answer=f"Voici mon conseil concernant '{request.question}': basez-vous sur les bonnes pratiques agricoles adaptées à votre niveau ({request.user_level}). N'hésitez pas à consulter vos formateurs pour des conseils spécifiques à votre région et votre filière.",
            question_echo=request.question,
            confidence=0.85,
            sources=["Base de connaissances MFR", "Expertise pédagogique"]
        )
        
    except Exception as e:
        logger.error("Error generating guidance", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Une erreur est survenue lors de la génération du conseil"
        )

# Activity suggestions endpoint
@app.post("/api/v1/suggestions", response_model=SuggestionResponse)
async def get_activity_suggestions(request: SuggestionRequest):
    """Get AI-powered activity suggestions based on user profile"""
    logger.info("Suggestion request received", profile=request.user_profile)
    
    # Return structured suggestions
    suggestions = [
        {
            "title": "Découverte de l'agriculture biologique",
            "description": "Introduction aux principes de base de l'agriculture biologique",
            "category": "agriculture",
            "difficulty": "beginner"
        },
        {
            "title": "Gestion d'une exploitation agricole",
            "description": "Bases de la gestion économique d'une exploitation",
            "category": "management", 
            "difficulty": "intermediate"
        },
        {
            "title": "Élevage durable",
            "description": "Pratiques d'élevage respectueuses de l'environnement",
            "category": "elevage",
            "difficulty": "intermediate"
        }
    ]
    
    # Filter by category if specified
    if request.category:
        suggestions = [s for s in suggestions if s["category"] == request.category]
    
    # Filter by difficulty if specified
    if request.difficulty != "all":
        suggestions = [s for s in suggestions if s["difficulty"] == request.difficulty]
    
    return SuggestionResponse(
        suggestions=suggestions,
        reasoning=f"Suggestions adaptées à votre profil: {request.user_profile}"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )