from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import time
from .core.config import settings
from .core.logging import log_info, log_error
from .api import auth, users, activities, registrations

# Create limiter for rate limiting
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app
app = FastAPI(
    title="LaVidaLuca API",
    description="FastAPI backend for LaVidaLuca App - Agricultural activities platform for MFR students",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add rate limiting middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.render.com", "lavidaluca.fr", "*.lavidaluca.fr"]
    )


# Middleware for logging requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    log_info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        log_info(f"Response: {response.status_code} - {process_time:.3f}s")
        
        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
    except Exception as e:
        process_time = time.time() - start_time
        log_error(f"Request failed: {str(e)} - {process_time:.3f}s")
        raise


# Health check endpoint
@app.get("/health")
@limiter.limit("100/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.environment
    }


# Root endpoint
@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):
    """Root endpoint with API information."""
    return {
        "message": "LaVidaLuca API",
        "description": "FastAPI backend for agricultural activities platform",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Include API routers
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(activities.router, prefix=settings.api_v1_prefix)
app.include_router(registrations.router, prefix=settings.api_v1_prefix)


# Startup event
@app.on_event("startup")
async def startup_event():
    log_info("LaVidaLuca API starting up...")
    log_info(f"Environment: {settings.environment}")
    log_info(f"CORS origins: {settings.cors_origins}")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    log_info("LaVidaLuca API shutting down...")