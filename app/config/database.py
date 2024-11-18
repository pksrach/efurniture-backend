from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from app.config.settings import get_settings

settings = get_settings()

# Add connect_args to disable statement caching
engine = create_async_engine(
    settings.DATABASE_URI,
    echo=True,
    connect_args={"statement_cache_size": 0}  # Disables prepared statement caching
)

async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
