"""
Core configuration for the LaVidaLuca FastAPI application.
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/lavidaluca")
    database_pool_size: int = 5
    database_max_overflow: int = 10
    
    # JWT Authentication
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "https://la-vida-luca.vercel.app"]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: List[str] = ["*"]
    
    # Application
    app_name: str = "LaVidaLuca API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_methods", pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [method.strip() for method in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()