"""
Main FastAPI application for LaVidaLuca API.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.api import api_router
from app.middleware.error_handling import ErrorHandlingMiddleware, LoggingMiddleware
# Import models to ensure they are registered
from app.models import User, Activity, Recommendation

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API backend for LaVidaLuca - Agricultural education and activity management platform",
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Add custom middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to LaVidaLuca API",
        "version": settings.app_version,
        "docs": "/docs" if settings.debug else "Documentation not available in production"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"detail": f"The endpoint {request.url.path} was not found"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )