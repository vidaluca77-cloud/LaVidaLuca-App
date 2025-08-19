from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openai_api_key: str
    allowed_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

    @property
    def allowed_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()