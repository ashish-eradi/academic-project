# app/core/config.py
# Correct import for Pydantic V2
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Project Academic"
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # Add the missing API_V1_STR setting
    API_V1_STR: str = "/api/v1"
    
    # Database
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./academic.db"
    
    class Config:
        case_sensitive = True
        # env_file = ".env" # Uncomment if you use a .env file

settings = Settings()
