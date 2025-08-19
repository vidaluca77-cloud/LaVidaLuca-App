from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    DATABASE_URL: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # Application
    PROJECT_NAME: str = "La Vida Luca API"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # CORS - defined here to avoid parsing issues
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://la-vida-luca.vercel.app",
        "https://*.vercel.app"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()