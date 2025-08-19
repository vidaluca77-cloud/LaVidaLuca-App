import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # FastAPI
    app_name: str = "La Vida Luca API"
    debug: bool = False
    api_v1_str: str = "/api/v1"
    
    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "https://la-vida-luca.vercel.app"]
    
    class Config:
        env_file = ".env"

settings = Settings()