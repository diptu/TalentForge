"""Async SQLAlchemy session for PostgreSQL using asyncpg."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from app.core.config import settings

# Async engine for NeonDB
engine = create_async_engine(
    settings.database.uri,
    echo=True,
    connect_args={"ssl": "require"},
)

# Async session factory with proper typing
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async database session."""
    async with AsyncSessionLocal() as session:
        yield session
