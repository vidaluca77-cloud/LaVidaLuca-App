from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import os
from datetime import datetime

# Initialize Sentry for error tracking
if os.getenv("SENTRY_DSN"):
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=os.getenv("ENVIRONMENT", "development"),
    )

app = FastAPI(
    title="La Vida Luca IA API",
    description="API d'intelligence artificielle pour La Vida Luca",
    version="1.0.0",
    docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
    redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None,
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[
        "localhost",
        "127.0.0.1",
        "la-vida-luca-ia.onrender.com",
        "la-vida-luca-ia-staging.onrender.com",
        "*.vercel.app",
    ]
)

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
if not allowed_origins or allowed_origins == [""]:
    allowed_origins = [
        "http://localhost:3000",
        "https://la-vida-luca.vercel.app",
        "https://la-vida-luca-staging.vercel.app",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "la-vida-luca-ia",
        "version": "1.0.0"
    }


@app.get("/api/v1/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "La Vida Luca IA",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "activities": "/api/v1/activities",
            "recommendations": "/api/v1/recommendations",
        }
    }


@app.get("/api/v1/activities")
async def get_activities():
    """Get available activities"""
    # This would connect to Supabase to fetch activities
    return {
        "activities": [
            {
                "id": "1",
                "title": "Soins aux animaux",
                "category": "agri",
                "description": "Nourrir, observer, nettoyer les espaces des animaux de la ferme.",
                "duration": 60,
                "difficulty": 1
            }
        ]
    }


@app.post("/api/v1/recommendations")
async def get_recommendations(user_preferences: dict):
    """Get activity recommendations based on user preferences"""
    # This would use AI to generate personalized recommendations
    return {
        "recommendations": [
            {
                "activity_id": "1",
                "score": 0.95,
                "reasons": ["Correspond à vos préférences", "Niveau adapté"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)