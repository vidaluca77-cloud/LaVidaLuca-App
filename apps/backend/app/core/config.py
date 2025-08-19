from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configuration de la base de données
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/lavidaluca"
    
    # Configuration de sécurité
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuration API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "La Vida Luca API"
    
    # Configuration CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://your-frontend-domain.vercel.app"
    ]
    
    # Configuration environnement
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()