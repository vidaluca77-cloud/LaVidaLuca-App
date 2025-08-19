"""
Application FastAPI principale pour La Vida Luca
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from datetime import datetime

from config import settings
from api.routes import activities, registrations

# Configuration du logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Création de l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API pour la plateforme La Vida Luca - Réseau de fermes autonomes & pédagogiques",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    openapi_url="/openapi.json" if settings.debug else None,
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de sécurité
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.onrender.com", "*.vercel.app", "lavidaluca.fr"]
    )

# Routes de l'API
app.include_router(
    activities.router,
    prefix=f"{settings.api_v1_prefix}/activities",
    tags=["Activités"]
)

app.include_router(
    registrations.router,
    prefix=f"{settings.api_v1_prefix}/registrations",
    tags=["Inscriptions"]
)

# Route de santé
@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version,
        "environment": settings.environment
    }

# Route de base
@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API La Vida Luca",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation non disponible en production",
        "health": "/health"
    }

# Gestionnaire d'erreur global
@app.exception_handler(500)
async def internal_server_error(request, exc):
    logger.error(f"Erreur interne du serveur: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Erreur interne du serveur",
            "message": "Une erreur inattendue s'est produite."
        }
    )

# Événements de démarrage et d'arrêt
@app.on_event("startup")
async def startup_event():
    logger.info(f"🚀 Démarrage de {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Arrêt de l'application")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )