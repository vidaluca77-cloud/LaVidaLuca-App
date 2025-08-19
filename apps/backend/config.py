from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    app_name: str = "LaVidaLuca Backend API"
    version: str = "1.0.0"
    debug: bool = False
    
    # Database (Supabase PostgreSQL)
    database_url: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    allowed_origins: list[str] = ["http://localhost:3000", "https://*.vercel.app"]
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # External services
    contact_email: str = "contact@lavidaluca.org"
    contact_phone: str = "+33 X XX XX XX XX"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()