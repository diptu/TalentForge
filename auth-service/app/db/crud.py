# app/db/crud.py
"""Async CRUD operations for User and related models."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import hash_password
from app.db import models, schemas

# -----------------------------
# User CRUD
# -----------------------------


async def get_user_by_email(db: AsyncSession, email: str) -> models.User | None:
    """Fetch a user by email."""
    result = await db.execute(select(models.User).where(models.User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User | None:
    """Fetch a user by ID."""
    result = await db.execute(select(models.User).where(models.User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user (with hashed password)."""
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_pw)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def list_users(
    db: AsyncSession, skip: int = 0, limit: int = 10
) -> list[models.User]:
    """Return paginated list of users."""
    result = await db.execute(select(models.User).offset(skip).limit(limit))
    return result.scalars().all()
