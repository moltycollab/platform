from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import List, Optional

class Settings(BaseSettings):
    # API configuration
    PROJECT_NAME: str = "MoltyCollab"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    # GitHub App configuration
    # Estos valores se obtendrán de .env en producción
    GITHUB_APP_ID: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_WEBHOOK_SECRET: Optional[str] = None
    
    # Auth configuration
    JWT_SECRET: str = "molty-secret-key-placeholder"  # Cambiar en producción
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana
    
    # Database configuration
    DATABASE_URL: str = "sqlite:///./sql_app.db"  # SQLite por defecto para desarrollo
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
