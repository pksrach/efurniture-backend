import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # App
    APP_NAME: str = os.environ.get("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.environ.get("DEBUG", False))
    TIMEZONE: str = os.environ.get("TIMEZONE", "Asia/Phnom_Penh")

    # Postgresql Database Config
    PG_PORT: str = os.environ.get("POSTGRES_PORT", "5432")
    PG_HOST: str = os.environ.get("POSTGRES_HOST")
    PG_USER: str = os.environ.get("POSTGRES_USER")
    PG_PASSWORD: str = os.environ.get("POSTGRES_PASSWORD")
    PG_DB: str = os.environ.get("POSTGRES_DATABASE")
    DATABASE_URI: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 30))

    # Email Config
    MAILTRAP_TEST_TOKEN: str = os.environ.get("MAILTRAP_TEST_TOKEN", "fake_mailtrap_token")

@lru_cache()
def get_settings() -> Settings:
    return Settings()