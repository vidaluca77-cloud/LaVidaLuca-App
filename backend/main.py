"""
Main FastAPI application for La Vida Luca backend.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from database.database import create_tables
from routers import auth, activities, users, suggestions
from monitoring.logger import context_logger
from monitoring.metrics import metrics_middleware, set_app_info
from docs.openapi import setup_docs

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    Handles startup and shutdown events.
    """
    # Startup
    context_logger.info("Starting La Vida Luca backend...")
    
    # Initialize database
    await create_tables()
    
    # Set application info for metrics
    set_app_info(
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development"),
        build_date=os.getenv("BUILD_DATE", "unknown")
    )
    
    context_logger.info("Backend startup complete")
    
    yield
    
    # Shutdown
    context_logger.info("Shutting down La Vida Luca backend...")


app = FastAPI(
    title="La Vida Luca API",
    description="API for La Vida Luca collaborative platform",
    version="1.0.0",
    lifespan=lifespan
)

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add metrics middleware
app.middleware("http")(metrics_middleware)

# Setup API documentation
setup_docs(app)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(activities.router, prefix="/api/activities", tags=["activities"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(suggestions.router, prefix="/api/suggestions", tags=["suggestions"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "La Vida Luca API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
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
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("ENVIRONMENT") == "development"
    )