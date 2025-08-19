"""
OpenAPI configuration for LaVidaLuca Backend API.
This module configures OpenAPI documentation including security schemes,
metadata, and Swagger UI customization.
"""

from typing import Dict, Any
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

# OpenAPI metadata
TITLE = "LaVidaLuca Backend API"
VERSION = "1.0.0"
DESCRIPTION = """
**LaVidaLuca Backend API** - Educational platform for MFR (Maisons Familiales Rurales) training programs.

## Overview

This API provides comprehensive functionality for managing educational activities, user authentication, 
AI-powered suggestions, and collaborative learning features.

## Features

* **User Management** - Registration, authentication, and profile management
* **Activity Management** - Create, read, update, and delete educational activities
* **AI Suggestions** - Intelligent activity recommendations powered by OpenAI
* **Collaborative Features** - Share activities and get personalized suggestions

## Authentication

This API uses JWT (JSON Web Token) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-token-here>
```

To get a token, use the `/auth/login` endpoint with valid credentials.

## Activity Categories

- **Agriculture** - Farming techniques and agricultural practices
- **Technology** - Modern farming technology and digital tools  
- **Environment** - Sustainable practices and environmental conservation
- **Business** - Agricultural business and entrepreneurship
- **Community** - Social skills and community engagement

## Difficulty Levels

- **Beginner** - Introductory level activities
- **Intermediate** - Standard level activities requiring some experience
- **Advanced** - Expert level activities for experienced learners
"""

CONTACT = {
    "name": "LaVidaLuca Support",
    "email": "support@lavidaluca.com",
    "url": "https://lavidaluca.com"
}

LICENSE_INFO = {
    "name": "MIT License",
    "url": "https://opensource.org/licenses/MIT"
}

TAGS_METADATA = [
    {
        "name": "root",
        "description": "Root endpoints for API information and health checks",
    },
    {
        "name": "authentication",
        "description": "User authentication operations including registration and login",
        "externalDocs": {
            "description": "Authentication documentation",
            "url": "https://fastapi.tiangolo.com/tutorial/security/",
        },
    },
    {
        "name": "users",
        "description": "User management operations for profiles and user data",
    },
    {
        "name": "activities", 
        "description": "Educational activity management - create, read, update, delete activities",
    },
    {
        "name": "suggestions",
        "description": "AI-powered activity suggestions and recommendations",
    },
]

# Security schemes
SECURITY_SCHEMES = {
    "BearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token obtained from the login endpoint"
    }
}

# Servers configuration
SERVERS = [
    {
        "url": "http://localhost:8000",
        "description": "Development server"
    },
    {
        "url": "https://api.lavidaluca.com",
        "description": "Production server"
    }
]


def custom_openapi(app: FastAPI) -> Dict[str, Any]:
    """
    Generate custom OpenAPI schema with enhanced configuration.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        Custom OpenAPI schema dictionary
    """
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title=TITLE,
        version=VERSION,
        description=DESCRIPTION,
        routes=app.routes,
        tags=TAGS_METADATA,
        servers=SERVERS,
        contact=CONTACT,
        license_info=LICENSE_INFO,
    )
    
    # Add security schemes
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    openapi_schema["components"]["securitySchemes"] = SECURITY_SCHEMES
    
    # Add global security requirement for protected endpoints
    # This can be overridden per endpoint as needed
    openapi_schema["security"] = [{"BearerAuth": []}]
    
    # Add additional metadata
    openapi_schema["info"]["x-logo"] = {
        "url": "https://lavidaluca.com/logo.png",
        "altText": "LaVidaLuca Logo"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def configure_swagger_ui() -> Dict[str, Any]:
    """
    Configure Swagger UI with custom settings.
    
    Returns:
        Swagger UI configuration dictionary
    """
    return {
        "swagger_ui_parameters": {
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "none",
            "operationsSorter": "method",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "defaultModelsExpandDepth": 2,
            "defaultModelExpandDepth": 2,
            "tryItOutEnabled": True,
        }
    }