"""
Main FastAPI application for La Vida Luca.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import sqlalchemy

from .config import settings
from .database import engine
from .routes import auth, users, activities, contacts, suggestions, examples
from .middleware import setup_middleware
from .exceptions import setup_exception_handlers


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting La Vida Luca API...")
    logger.info("Database engine initialized")
    
    yield
    
    # Cleanup
    await engine.dispose()
    logger.info("Database engine disposed")
    logger.info("La Vida Luca API shutdown")


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
    app.include_router(examples.router, prefix="/api/v1/examples", tags=["examples"])
    
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
            async with engine.begin() as conn:
                await conn.execute(sqlalchemy.text("SELECT 1"))
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            db_status = "unhealthy"
        
        return {
            "status": "healthy",
            "database": db_status,
            "environment": settings.ENVIRONMENT
        }
    
    return app


# Create app instance
app = create_app()