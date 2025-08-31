# app/db/session.py
"""Async SQLAlchemy session for PostgreSQL using asyncpg."""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Async engine for NeonDB
engine = create_async_engine(
    settings.database.uri,  # e.g. 'postgresql+asyncpg://user:pass@host/dbname'
    future=True,
    echo=True,
    connect_args={"ssl": "require"},  # pass SSL here instead of in URI
)

# Async session factory
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncSession:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        yield session
