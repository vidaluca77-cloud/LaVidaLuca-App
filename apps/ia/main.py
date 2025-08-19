from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from database import engine
from database.models import Base
from routers import auth, users, activities, recommendations
from config import settings
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LaVidaLuca API",
    description="API backend for LaVidaLuca - Formation des jeunes en MFR",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


# Custom middleware for logging and timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    # Log response
    logger.info(f"Response: {response.status_code} - Time: {process_time:.4f}s")
    
    return response


# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "message": "Internal server error",
            "status_code": 500
        }
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "LaVidaLuca API",
        "version": "1.0.0"
    }


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API LaVidaLuca",
        "description": "API backend pour la formation des jeunes en MFR",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(activities.router)
app.include_router(recommendations.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)