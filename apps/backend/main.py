"""
Main FastAPI application for La Vida Luca with enhanced monitoring and security.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging
import os

from app.core.config import settings
from app.core.database import connect_database, disconnect_database, check_database_health
from app.core.monitoring import (
    init_sentry, MetricsMiddleware, get_health_metrics, 
    create_metrics_response, record_custom_metric
)

# Initialize Sentry
init_sentry()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" if settings.LOG_FORMAT != "json" else None
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Starting La Vida Luca API...")
    
    # Connect to database
    try:
        await connect_database()
        logger.info("Database connected successfully")
        record_custom_metric("app_startup", 1, {"component": "database"})
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
        logger.info("Starting API without database connection")
    
    # Record startup metric
    record_custom_metric("app_startup", 1, {"component": "api"})
    
    yield
    
    # Cleanup
    try:
        await disconnect_database()
        logger.info("Database disconnected successfully")
    except Exception as e:
        logger.warning(f"Database disconnect failed: {e}")
    
    logger.info("La Vida Luca API shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
        openapi_url="/openapi.json" if not settings.is_production else None,
    )
    
    # Add security middleware
    if settings.TRUSTED_HOSTS and settings.TRUSTED_HOSTS != ["*"]:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.TRUSTED_HOSTS
        )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    
    # Add metrics middleware
    if settings.PROMETHEUS_ENABLED:
        app.add_middleware(MetricsMiddleware)
    
    # Include API routes (will be added when they exist)
    # app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["authentication"])
    # app.include_router(users.router, prefix=settings.API_V1_STR + "/users", tags=["users"])
    # app.include_router(activities.router, prefix=settings.API_V1_STR + "/activities", tags=["activities"])
    # app.include_router(contacts.router, prefix=settings.API_V1_STR + "/contacts", tags=["contacts"])
    # app.include_router(suggestions.router, prefix=settings.API_V1_STR + "/suggestions", tags=["suggestions"])
    # app.include_router(guide.router, prefix=settings.API_V1_STR, tags=["guide"])
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Welcome to La Vida Luca API",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "docs": "/docs" if not settings.is_production else "disabled",
            "status": "healthy"
        }
    
    @app.get("/health")
    async def health_check():
        """Comprehensive health check endpoint."""
        db_health = await check_database_health()
        app_health = await get_health_metrics()
        
        overall_status = "healthy" if db_health["status"] == "healthy" else "degraded"
        
        return {
            "status": overall_status,
            "database": db_health,
            "application": app_health,
            "timestamp": "2024-01-01T00:00:00Z",  # Will be replaced with actual timestamp
        }
    
    # Add metrics endpoint
    @app.get("/metrics")
    async def metrics():
        """Prometheus metrics endpoint."""
        if not settings.PROMETHEUS_ENABLED:
            raise HTTPException(status_code=404, detail="Metrics not enabled")
        
        return create_metrics_response()
    
    @app.get("/info")
    async def app_info():
        """Application information endpoint."""
        return {
            "name": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "description": settings.DESCRIPTION,
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
            "api_version": settings.API_V1_STR,
        }
    
    return app


# Create app instance
app = create_app()