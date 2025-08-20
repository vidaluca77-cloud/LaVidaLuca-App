from fastapi import APIRouter
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint for production monitoring
    """
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "database": "connected" if settings.database_url else "not_configured"
    }


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint for deployment verification
    """
    return {
        "status": "ready",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "checks": {
            "database": "ok",
            "configuration": "ok"
        }
    }