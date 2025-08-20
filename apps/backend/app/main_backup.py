import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from .api.api import api_router
from .core.config import settings


def load_custom_openapi():
    """Load custom OpenAPI specification from docs/openapi.json"""
    docs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs", "openapi.json")
    try:
        with open(docs_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        swagger_ui_parameters={
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "none",
            "operationsSorter": "method",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
        }
    )

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

    # Custom OpenAPI configuration
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        
        # Try to load custom OpenAPI spec first
        custom_spec = load_custom_openapi()
        if custom_spec:
            app.openapi_schema = custom_spec
            return app.openapi_schema
        
        # Fallback to auto-generated OpenAPI
        openapi_schema = get_openapi(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            description=settings.DESCRIPTION,
            routes=app.routes,
        )
        
        # Add security scheme
        openapi_schema["components"]["securitySchemes"] = {
            "HTTPBearer": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "JWT token obtained from /auth/login endpoint"
            }
        }
        
        # Add tags
        openapi_schema["tags"] = [
            {
                "name": "Authentication",
                "description": "User authentication and authorization endpoints"
            },
            {
                "name": "Activities", 
                "description": "Learning activity management endpoints"
            },
            {
                "name": "Users",
                "description": "User management endpoints"
            },
            {
                "name": "Suggestions",
                "description": "AI-powered activity suggestion endpoints"
            },
            {
                "name": "Contacts",
                "description": "Contact form submission and management endpoints"
            }
        ]
        
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    @app.get("/")
    def root():
        return {
            "message": "Welcome to LaVidaLuca Backend API",
            "version": settings.VERSION,
            "docs": "/docs"
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy", "service": "lavidaluca-backend"}

    return app


app = create_app()