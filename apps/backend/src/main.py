"""
FastAPI main application for La Vida Luca backend.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time

from .core.config import settings
from .core.logger import setup_logging, context_logger
from .core.metrics import metrics_middleware, set_app_info, update_system_metrics
from .core.openapi import setup_docs
from .api.v1 import auth, users, activities, contact

# Setup logging
logger = setup_logging()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API pour la plateforme collaborative La Vida Luca",
    debug=settings.debug
)

# Setup documentation
setup_docs(app)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure this in production
)

# Add metrics middleware
@app.middleware("http")
async def add_metrics_middleware(request: Request, call_next):
    return await metrics_middleware(request, call_next)

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(activities.router, prefix="/api/v1")
app.include_router(contact.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("Starting La Vida Luca backend")
    
    # Set application info for metrics
    set_app_info(
        version=settings.app_version,
        environment=settings.environment,
        build_date=str(int(time.time()))
    )
    
    logger.info("Application started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Shutting down La Vida Luca backend")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "message": "Bienvenue dans l'API La Vida Luca !"
    }


@app.get("/health", response_model=dict)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": settings.app_version,
        "environment": settings.environment
    }


@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint."""
    # Update system metrics before returning
    update_system_metrics()
    
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    context_logger.error(
        "Unhandled exception",
        exception=str(exc),
        path=request.url.path,
        method=request.method
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An internal server error occurred"
            }
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )