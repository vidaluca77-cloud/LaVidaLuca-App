"""
OpenAPI documentation configuration for La Vida Luca API.
Provides comprehensive API documentation with examples and schemas.
"""

from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """
    Generate custom OpenAPI schema with enhanced documentation.
    
    Args:
        app: FastAPI application instance
        
    Returns:
        OpenAPI schema dictionary
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="La Vida Luca API",
        version="1.0.0",
        description="""
# La Vida Luca API

API pour la plateforme collaborative La Vida Luca dédiée à la formation des jeunes en MFR 
et au développement d'une agriculture nouvelle.

## Authentification

L'API utilise l'authentification JWT via Supabase. Incluez le token dans l'en-tête Authorization :

```
Authorization: Bearer <your-jwt-token>
```

## Codes de statut

- **200** : Succès
- **201** : Créé avec succès
- **400** : Erreur de validation
- **401** : Non authentifié
- **403** : Non autorisé
- **404** : Ressource non trouvée
- **422** : Erreur de validation des données
- **500** : Erreur serveur

## Limites de taux

- **100 requêtes/minute** pour les utilisateurs authentifiés
- **20 requêtes/minute** pour les utilisateurs non authentifiés

## Exemples de réponses

### Succès
```json
{
  "success": true,
  "data": { ... },
  "message": "Opération réussie"
}
```

### Erreur
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Données invalides",
    "details": { ... }
  }
}
```
        """,
        routes=app.routes,
        contact={
            "name": "Équipe La Vida Luca",
            "email": "tech@lavidaluca.fr",
            "url": "https://lavidaluca.fr"
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        servers=[
            {
                "url": "https://api.lavidaluca.fr",
                "description": "Production"
            },
            {
                "url": "https://staging-api.lavidaluca.fr",
                "description": "Staging"
            },
            {
                "url": "http://localhost:8000",
                "description": "Development"
            }
        ]
    )
    
    # Add custom schemas
    openapi_schema["components"]["schemas"].update({
        "Activity": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Identifiant unique de l'activité",
                    "example": "act_abc123"
                },
                "title": {
                    "type": "string",
                    "description": "Titre de l'activité",
                    "example": "Culture de légumes biologiques"
                },
                "category": {
                    "type": "string",
                    "enum": ["agri", "transfo", "artisanat", "nature", "social"],
                    "description": "Catégorie de l'activité"
                },
                "summary": {
                    "type": "string",
                    "description": "Résumé de l'activité",
                    "example": "Apprentissage des techniques de culture biologique"
                },
                "duration_min": {
                    "type": "integer",
                    "description": "Durée en minutes",
                    "example": 120
                },
                "skill_tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Compétences associées",
                    "example": ["jardinage", "biologie", "écologie"]
                },
                "safety_level": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 5,
                    "description": "Niveau de sécurité (1=très sûr, 5=risqué)",
                    "example": 2
                },
                "materials": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Matériel nécessaire",
                    "example": ["bêche", "graines", "arrosoir"]
                }
            },
            "required": ["id", "title", "category", "summary", "duration_min"]
        },
        "User": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Identifiant unique de l'utilisateur",
                    "example": "user_xyz789"
                },
                "email": {
                    "type": "string",
                    "format": "email",
                    "description": "Adresse email",
                    "example": "user@example.com"
                },
                "profile": {
                    "type": "object",
                    "properties": {
                        "skills": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Compétences de l'utilisateur"
                        },
                        "availability": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Disponibilités"
                        },
                        "location": {
                            "type": "string",
                            "description": "Localisation"
                        }
                    }
                }
            },
            "required": ["id", "email"]
        },
        "Suggestion": {
            "type": "object",
            "properties": {
                "activity": {"$ref": "#/components/schemas/Activity"},
                "score": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": "Score de pertinence (0-1)",
                    "example": 0.85
                },
                "reasons": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Raisons de la suggestion",
                    "example": ["Correspond à vos compétences", "Dans votre région"]
                }
            },
            "required": ["activity", "score", "reasons"]
        },
        "ApiResponse": {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Statut de la réponse"
                },
                "data": {
                    "description": "Données de la réponse"
                },
                "message": {
                    "type": "string",
                    "description": "Message descriptif"
                }
            },
            "required": ["success"]
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Statut de la réponse",
                    "example": False
                },
                "error": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "Code d'erreur",
                            "example": "VALIDATION_ERROR"
                        },
                        "message": {
                            "type": "string",
                            "description": "Message d'erreur",
                            "example": "Données invalides"
                        },
                        "details": {
                            "description": "Détails de l'erreur"
                        }
                    },
                    "required": ["code", "message"]
                }
            },
            "required": ["success", "error"]
        }
    })
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token via Supabase authentication"
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

def setup_docs(app: FastAPI):
    """
    Configure API documentation for the FastAPI app.
    
    Args:
        app: FastAPI application instance
    """
    app.openapi = lambda: custom_openapi(app)
    
    # Add custom CSS for docs
    app.docs_url = "/docs"
    app.redoc_url = "/redoc"