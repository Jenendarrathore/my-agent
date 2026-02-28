from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    
    SECRET_KEY: str = "your-super-secret-key-change-it"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BACKEND_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:5174"

    GOOGLE_CLIENT_ID: str = "GOOGLE_CLIENT_ID"
    GOOGLE_CLIENT_SECRET: str = "GOOGLE_CLIENT_SECRET"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"

settings = Settings()
