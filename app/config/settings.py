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

    # Postgresql Database Config
    PG_HOST: str = os.environ.get("PG_HOST")
    PG_USER: str = os.environ.get("PG_USER")
    PG_PASSWORD: str = os.environ.get("PG_PASSWORD")
    PG_DB: str = os.environ.get("PG_DB")
    DATABASE_URI: str = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}/{PG_DB}"

    # JWT Secret Key
    JWT_SECRET: str = os.environ.get("JWT_SECRET_KEY", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = os.environ.get("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 3))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 30))

    # Email Config
    MAILTRAP_TEST_TOKEN: str = os.environ.get("MAILTRAP_TEST_TOKEN", "fake_mailtrap_token")

@lru_cache()
def get_settings() -> Settings:
    return Settings()