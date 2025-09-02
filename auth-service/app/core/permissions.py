# app/core/permissions.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User, UserRole
from app.db.session import get_db
from app.core.jwt import decode_token


async def get_current_user(token: str, db: AsyncSession = Depends(get_db)) -> User:
    """Get current user from JWT token."""
    from app.core.jwt import decode_token

    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    from app.db import crud

    user = await crud.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def require_roles(*roles: UserRole):
    """Dependency generator to require specific user roles."""

    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )
        return current_user

    return role_checker
