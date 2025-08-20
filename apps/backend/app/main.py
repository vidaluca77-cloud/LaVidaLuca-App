"""
Main FastAPI application module.

This module creates and configures the FastAPI application instance
with basic health check endpoints for the agricultural assistant.
"""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.app_name,
        description=settings.description,
        version=settings.version,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    @app.get("/")
    async def root():
        """
        Root endpoint providing basic API information.
        
        Returns:
            dict: Basic API information and status
        """
        return {
            "message": "Bienvenue sur l'API La Vida Luca",
            "version": settings.version,
            "description": settings.description,
            "docs": "/docs",
            "status": "healthy"
        }
    
    @app.get("/health")
    async def health_check(db: Session = Depends(get_db)):
        """
        Health check endpoint for monitoring application status.
        
        Args:
            db: Database session dependency
            
        Returns:
            dict: Application health status including database connectivity
        """
        try:
            # Test database connection with a simple query
            from sqlalchemy import text
            db.execute(text("SELECT 1"))
            db_status = "healthy"
        except Exception as e:
            db_status = "unhealthy"
            
        return {
            "status": "healthy" if db_status == "healthy" else "degraded",
            "database": db_status,
            "api_version": settings.version,
            "service": "agricultural_assistant"
        }
    
    return app


# Create application instance
app = create_app()