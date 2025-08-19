"""
Main FastAPI application for La Vida Luca.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database import database
from .routes import auth, users, activities, contacts, suggestions
from .middleware import setup_middleware
from .exceptions import setup_exception_handlers


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
        description="""
        ## 🌱 API pour la plateforme collaborative La Vida Luca

        La Vida Luca est une plateforme dédiée à la formation des jeunes en MFR (Maisons Familiales Rurales) 
        et au développement d'une agriculture vivante et respectueuse.

        ### Fonctionnalités principales

        * **🔐 Authentification** - Gestion des utilisateurs avec JWT
        * **🎯 Activités** - Catalogue de 30+ activités pédagogiques
        * **🤖 Suggestions IA** - Recommandations personnalisées basées sur les profils
        * **📧 Contact** - Gestion des demandes de contact et d'inscription
        * **👥 Utilisateurs** - Profils et préférences des participants

        ### Architecture technique

        * **Backend**: FastAPI + Python 3.11+
        * **Base de données**: PostgreSQL avec SQLAlchemy (async)
        * **Authentification**: JWT (JSON Web Tokens)
        * **IA**: OpenAI GPT pour les suggestions personnalisées
        * **Monitoring**: Sentry pour le tracking d'erreurs

        ### Sécurité

        * Authentification par tokens JWT
        * Hashage sécurisé des mots de passe (bcrypt)
        * Validation des données avec Pydantic
        * Protection CORS configurée
        * Rate limiting sur les endpoints sensibles

        ### Utilisation

        1. **Inscription/Connexion** via `/api/v1/auth/`
        2. **Exploration du catalogue** via `/api/v1/activities/`
        3. **Suggestions personnalisées** via `/api/v1/suggestions/`
        4. **Contact** via `/api/v1/contacts/`

        Pour plus d'informations, consultez notre [documentation complète](https://github.com/vidaluca77-cloud/LaVidaLuca-App).
        """,
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
        
        # OpenAPI configuration
        openapi_tags=[
            {
                "name": "authentication",
                "description": "🔐 Gestion de l'authentification et des sessions utilisateur",
            },
            {
                "name": "users",
                "description": "👥 Gestion des profils utilisateurs et préférences",
            },
            {
                "name": "activities",
                "description": "🎯 Catalogue d'activités pédagogiques et agricoles",
            },
            {
                "name": "suggestions",
                "description": "🤖 Recommandations personnalisées par IA",
            },
            {
                "name": "contacts",
                "description": "📧 Gestion des demandes de contact et d'inscription",
            },
        ],
        
        # Contact information
        contact={
            "name": "Équipe La Vida Luca",
            "email": "vidaluca77@gmail.com",
            "url": "https://github.com/vidaluca77-cloud/LaVidaLuca-App",
        },
        
        # License information
        license_info={
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT",
        },
        
        # Terms of service
        terms_of_service="https://github.com/vidaluca77-cloud/LaVidaLuca-App/blob/main/LICENSE",
        
        # Servers information for different environments
        servers=[
            {
                "url": "http://localhost:8000",
                "description": "Serveur de développement local"
            },
            {
                "url": "https://lavidaluca-api.render.com",
                "description": "Serveur de production"
            }
        ]
    )
    
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