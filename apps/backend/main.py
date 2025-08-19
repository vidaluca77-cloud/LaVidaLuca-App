"""
Main FastAPI application for La Vida Luca.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import os

from .config import settings
from .database import database
from .routes import auth, users, activities, contacts, suggestions
from .middleware import setup_middleware
from .exceptions import setup_exception_handlers
from .monitoring import (
    init_sentry, setup_logging, context_logger, set_app_info, 
    update_system_metrics, APP_INFO
)

# Initialize monitoring
init_sentry(
    environment=settings.ENVIRONMENT,
    release=os.getenv("RELEASE_VERSION", "1.0.0")
)

# Setup structured logging
app_logger = setup_logging("la-vida-luca-backend")

# Set application info for metrics
set_app_info(
    version="1.0.0",
    environment=settings.ENVIRONMENT,
    build_date=os.getenv("BUILD_DATE", "unknown")
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    context_logger.info("Starting La Vida Luca API...")
    
    # Connect to database
    await database.connect()
    context_logger.info("Database connected")
    
    # Update system metrics on startup
    update_system_metrics()
    
    yield
    
    # Cleanup
    await database.disconnect()
    context_logger.info("Database disconnected")
    context_logger.info("La Vida Luca API shutdown")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="La Vida Luca API",
        description="API pour la plateforme collaborative La Vida Luca",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    )
    
    # Setup middleware
    setup_middleware(app)
    
    # Setup exception handlers
    setup_exception_handlers(app)
    
    # Include routes
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
    app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
    app.include_router(contacts.router, prefix="/api/v1/contacts", tags=["contacts"])
    app.include_router(suggestions.router, prefix="/api/v1/suggestions", tags=["suggestions"])
    
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
        try:
            # Test database connection
            await database.execute("SELECT 1")
            db_status = "healthy"
        except Exception as e:
            context_logger.error("Database health check failed", error=str(e))
            db_status = "unhealthy"
        
        return {
            "status": "healthy",
            "database": db_status,
            "environment": settings.ENVIRONMENT
        }
    
    # Add metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from fastapi import Response
        
        # Update system metrics before serving
        update_system_metrics()
        
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )
    
    return app


# Create app instance
app = create_app()