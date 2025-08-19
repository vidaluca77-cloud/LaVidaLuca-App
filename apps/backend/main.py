"""
FastAPI main application for La Vida Luca backend.
Provides API endpoints for activities, authentication, and AI suggestions.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
import sys
from pathlib import Path

# Add the parent directory to Python path to import monitoring utilities
parent_dir = Path(__file__).parent.parent.parent / "backend"
sys.path.append(str(parent_dir))

from routers import auth, activities
from database import engine, Base
from monitoring.metrics import metrics_middleware, set_app_info

# Import monitoring utilities
try:
    from monitoring.logger import setup_logging, context_logger
    from monitoring.metrics import set_app_info
    logger = setup_logging("la-vida-luca-backend")
except ImportError:
    # Fallback if monitoring utilities aren't available
    import logging
    logger = logging.getLogger(__name__)
    context_logger = logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting La Vida Luca Backend API")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Set application info for metrics
    set_app_info(
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development"),
        build_date="2024-01-01"
    )
    
    yield
    
    # Shutdown
    logger.info("Shutting down La Vida Luca Backend API")

# Create FastAPI application
app = FastAPI(
    title="La Vida Luca API",
    description="API for La Vida Luca collaborative platform for young farmers education",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        "https://lavidaluca.fr",  # Production frontend
        "https://*.vercel.app",   # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(activities.router, prefix="/api/activities", tags=["Activities"])

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "La Vida Luca API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "la-vida-luca-backend",
        "version": "1.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for proper error responses."""
    context_logger.error(
        f"Unhandled exception: {str(exc)}",
        request_id=getattr(request.state, "request_id", None),
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
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )