"""
Main FastAPI application for La Vida Luca.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database import database
from .routes import auth, users, activities, contacts, suggestions
from .middleware import setup_middleware
from .exceptions import setup_exception_handlers
from .schemas.errors import COMMON_ERROR_RESPONSES
from .schemas.rate_limits import RATE_LIMIT_DOCUMENTATION


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
    
    # Connect to database
    await database.connect()
    logger.info("Database connected")
    
    yield
    
    # Cleanup
    await database.disconnect()
    logger.info("Database disconnected")
    logger.info("La Vida Luca API shutdown")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    app = FastAPI(
        title="La Vida Luca API",
        description="API for La Vida Luca platform - farm network and educational platform",
        version="1.0.0",
        lifespan=lifespan,
        openapi_url="/openapi.json",
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
    )
    
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="La Vida Luca API",
            version="1.0.0",
            description="""
# La Vida Luca API

Complete API documentation for La Vida Luca platform - a farm network and educational platform connecting people with sustainable agriculture and rural life learning experiences.

## Features

- **User Authentication**: JWT-based authentication system
- **Educational Activities**: Create, discover, and participate in learning activities
- **AI-Powered Suggestions**: Personalized activity recommendations using OpenAI
- **Contact Management**: Public contact forms and admin management
- **User Profiles**: Comprehensive user management and profiles

## Authentication

Most endpoints require authentication using JWT Bearer tokens. Include your token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

Get your token by calling the `/api/v1/auth/login` endpoint with valid credentials.

## Rate Limiting

This API implements comprehensive rate limiting. See the Rate Limiting section below for details.

## Error Handling

All errors follow a consistent format with appropriate HTTP status codes and descriptive messages.
            """,
            routes=app.routes,
        )
        
        # Add logo
        openapi_schema["info"]["x-logo"] = {
            "url": "https://la-vida-luca.vercel.app/logo.png"
        }
        
        # Add contact information
        openapi_schema["info"]["contact"] = {
            "name": "La Vida Luca Support",
            "email": "support@lavidaluca.com",
            "url": "https://la-vida-luca.vercel.app"
        }
        
        # Add license information
        openapi_schema["info"]["license"] = {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
        
        # Add server information
        openapi_schema["servers"] = [
            {
                "url": "https://api.lavidaluca.com",
                "description": "Production server"
            },
            {
                "url": "https://staging-api.lavidaluca.com",
                "description": "Staging server"
            },
            {
                "url": "http://localhost:8000",
                "description": "Development server"
            }
        ]
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT token for API authentication. Include 'Bearer ' prefix."
            }
        }
        
        # Add common error response schemas
        if "components" not in openapi_schema:
            openapi_schema["components"] = {}
        if "responses" not in openapi_schema["components"]:
            openapi_schema["components"]["responses"] = {}
            
        # Add error response schemas
        openapi_schema["components"]["responses"].update({
            "BadRequest": COMMON_ERROR_RESPONSES[400],
            "Unauthorized": COMMON_ERROR_RESPONSES[401],
            "Forbidden": COMMON_ERROR_RESPONSES[403],
            "NotFound": COMMON_ERROR_RESPONSES[404],
            "Conflict": COMMON_ERROR_RESPONSES[409],
            "ValidationError": COMMON_ERROR_RESPONSES[422],
            "TooManyRequests": COMMON_ERROR_RESPONSES[429],
            "InternalServerError": COMMON_ERROR_RESPONSES[500],
            "ServiceUnavailable": COMMON_ERROR_RESPONSES[503]
        })
        
        # Add tags for organization
        openapi_schema["tags"] = [
            {
                "name": "Authentication",
                "description": "User authentication and token management"
            },
            {
                "name": "User Management", 
                "description": "User profile and account management"
            },
            {
                "name": "Activities",
                "description": "Educational activities and learning experiences"
            },
            {
                "name": "Contact",
                "description": "Contact forms and communication"
            },
            {
                "name": "AI Suggestions",
                "description": "AI-powered activity recommendations"
            }
        ]
        
        # Add rate limiting documentation as extension
        openapi_schema["x-rate-limiting"] = RATE_LIMIT_DOCUMENTATION
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
    
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