from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "LaVidaLuca Backend"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Backend API for LaVidaLuca - MFR training platform"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: Optional[str] = None
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "lavidaluca"
    POSTGRES_PORT: int = 5432
    
    # Security
    SECRET_KEY: str = "super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    
    # CORS Configuration
    ALLOWED_HOSTS: List[str] = ["*"]
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "https://lavidaluca.vercel.app",
        "https://*.vercel.app"
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Sentry Configuration for Backend Monitoring
    SENTRY_DSN: Optional[str] = None
    SENTRY_ENVIRONMENT: Optional[str] = None
    SENTRY_RELEASE: Optional[str] = None
    SENTRY_TRACES_SAMPLE_RATE: float = 0.1
    
    # Production Security Settings
    SECURE_COOKIES: bool = False
    SECURE_HEADERS: bool = False
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Health Check
    HEALTH_CHECK_ENABLED: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list, handling both string and list inputs"""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    def configure_for_production(self):
        """Configure settings for production environment"""
        if self.is_production:
            self.DEBUG = False
            self.SECURE_COOKIES = True
            self.SECURE_HEADERS = True
            # Remove wildcard from allowed hosts in production
            if "*" in self.ALLOWED_HOSTS:
                self.ALLOWED_HOSTS = [
                    "lavidaluca-backend.onrender.com",
                    "localhost"
                ]


settings = Settings()

# Auto-configure for production
if settings.is_production:
    settings.configure_for_production()