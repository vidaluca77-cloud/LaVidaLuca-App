from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.api import api_router
from .core.config import settings


def create_app() -> FastAPI:
    """Create and configure the FastAPI application with enhanced OpenAPI documentation."""
    
    # Import OpenAPI configuration from the new location
    import sys
    import os
    # Add the parent directory to sys.path to import from /apps/backend/api/
    backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if backend_path not in sys.path:
        sys.path.append(backend_path)
    
    try:
        from api.openapi import custom_openapi, configure_swagger_ui, TAGS_METADATA
    except ImportError:
        # Fallback if the import doesn't work
        TAGS_METADATA = [
            {"name": "root", "description": "Root endpoints for API information and health checks"},
            {"name": "authentication", "description": "User authentication operations"},
            {"name": "users", "description": "User management operations"},
            {"name": "activities", "description": "Educational activity management"},
            {"name": "suggestions", "description": "AI-powered activity suggestions"},
        ]
        custom_openapi = None
        configure_swagger_ui = lambda: {}
    
    # Create FastAPI app with enhanced configuration
    swagger_config = configure_swagger_ui() if 'configure_swagger_ui' in locals() else {}
    app = FastAPI(
        title="LaVidaLuca Backend API",
        version="1.0.0",
        description="Educational platform for MFR (Maisons Familiales Rurales) training programs",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_tags=TAGS_METADATA,
        contact={
            "name": "LaVidaLuca Support",
            "email": "support@lavidaluca.com",
            "url": "https://lavidaluca.com"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        **swagger_config
    )

    # Set custom OpenAPI schema if available
    if custom_openapi:
        app.openapi = lambda: custom_openapi(app)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get(
        "/",
        summary="API Root",
        description="Welcome endpoint providing basic API information and navigation links",
        responses={
            200: {
                "description": "API information successfully retrieved",
                "content": {
                    "application/json": {
                        "example": {
                            "message": "Welcome to LaVidaLuca Backend API",
                            "version": "1.0.0",
                            "docs": "/docs",
                            "redoc": "/redoc",
                            "openapi": "/api/v1/openapi.json"
                        }
                    }
                }
            }
        },
        tags=["root"]
    )
    def root():
        """API root endpoint with basic information."""
        return {
            "message": "Welcome to LaVidaLuca Backend API",
            "version": settings.VERSION,
            "docs": "/docs",
            "redoc": "/redoc", 
            "openapi": f"{settings.API_V1_STR}/openapi.json"
        }

    @app.get(
        "/health",
        summary="Health Check",
        description="Simple health check endpoint to verify API availability",
        responses={
            200: {
                "description": "API is healthy and operational",
                "content": {
                    "application/json": {
                        "example": {
                            "status": "healthy",
                            "service": "lavidaluca-backend",
                            "version": "1.0.0"
                        }
                    }
                }
            }
        },
        tags=["root"]
    )
    def health_check():
        """Health check endpoint."""
        return {
            "status": "healthy", 
            "service": "lavidaluca-backend",
            "version": settings.VERSION
        }

    return app


app = create_app()