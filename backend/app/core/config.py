from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    app_name: str = "Enterprise RAG Platform"
    database_url: str = "postgresql+psycopg2://raguser:ragpass@localhost:5432/ragdb"
    jwt_secret: str = "change-me-now"
    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501"
    upload_dir: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    @property
    def cors_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

settings = Settings()
