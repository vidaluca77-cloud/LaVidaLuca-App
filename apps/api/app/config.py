from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/lavidaluca"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # JWT
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OpenAI
    openai_api_key: str = ""
    
    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "https://localhost:3000"]
    
    # Environment
    environment: str = "development"
    
    class Config:
        env_file = ".env"


settings = Settings()