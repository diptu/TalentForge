"""
File: app/api/v1/auth/router.py
Authentication endpoints with JWT, Redis-based rate limiting, and robust error handling.
"""

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.hashing import hash_password, verify_password
from app.core.rate_limiter import RateLimiter, get_rate_limiter
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db import crud
from app.db.models import User, UserRole
from app.db.schemas import UserCreate, UserLogin
from app.db.session import get_db
from app.services.token_blacklist import add_to_blacklist, is_blacklisted
from app.utils.response import error_response, success_response

from .schemas import TokenLogoutRequest, TokenRefreshRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    limiter: RateLimiter = Depends(get_rate_limiter),
    role: Optional[UserRole] = UserRole.USER,
) -> Dict[str, Any]:
    """Register a new user (rate limited per IP)."""
    try:
        await limiter.check(request)

        existing_user = await crud.get_user_by_email(db, user.email)
        if existing_user:
            return error_response(
                code=status.HTTP_400_BAD_REQUEST,
                message="User with this email already exists",
            )

        hashed_pw = hash_password(user.password)
        new_user = User(email=user.email, hashed_password=hashed_pw, role=role)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        data = {"user_id": new_user.id, "role": new_user.role.value}
        return success_response(data=data, message="User registered successfully")

    except Exception as exc:
        return error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Registration failed due to internal error",
            details=str(exc),
        )


@router.post("/login")
async def login(
    request: Request,
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
    limiter: RateLimiter = Depends(get_rate_limiter),
) -> Dict[str, Any]:
    """Authenticate user and return JWT tokens (rate limited per IP + email)."""
    try:
        await limiter.check(request, identifier=user.email)

        db_user = await crud.get_user_by_email(db, user.email)
        if not db_user or not isinstance(db_user.hashed_password, str):
            return error_response(
                code=status.HTTP_401_UNAUTHORIZED, message="Invalid credentials"
            )

        if not verify_password(user.password, db_user.hashed_password):
            return error_response(
                code=status.HTTP_401_UNAUTHORIZED, message="Invalid credentials"
            )

        access_token = create_access_token(email=db_user.email, role=db_user.role.value)
        refresh_token, _ = create_refresh_token(
            email=db_user.email, role=db_user.role.value
        )

        data = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": db_user.role.value,
            "email": db_user.email,
        }
        return success_response(data=data, message="Login successful")

    except Exception as exc:
        return error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Login failed due to internal error",
            details=str(exc),
        )


@router.post("/refresh")
async def refresh_token(token_request: TokenRefreshRequest) -> Dict[str, Any]:
    """Refresh access token using a valid refresh token."""
    try:
        payload = decode_token(token_request.refresh_token)
        jti: str = payload.get("jti", "")
        if jti and await is_blacklisted(jti):
            return error_response(
                code=status.HTTP_401_UNAUTHORIZED, message="Refresh token revoked"
            )

        email: str = payload.get("email", "")
        role: str = payload.get("role", "user")
        if not email:
            return error_response(
                code=status.HTTP_401_UNAUTHORIZED, message="Invalid token payload"
            )

        access_token = create_access_token(email=email, role=role)
        data = {
            "access_token": access_token,
            "refresh_token": None,
            "token_type": "bearer",
            "role": role,
            "email": email,
        }
        return success_response(data=data, message="Access token refreshed")

    except Exception as exc:
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Refresh token invalid or expired",
            details=str(exc),
        )


@router.post("/logout")
async def logout(token_request: TokenLogoutRequest) -> Dict[str, Any]:
    """Invalidate refresh token by adding it to blacklist."""
    try:
        payload = decode_token(token_request.refresh_token)
        jti: str = payload.get("jti")
        exp: int = payload.get("exp", 0)
        if not jti or not exp:
            return error_response(
                code=status.HTTP_400_BAD_REQUEST, message="Malformed refresh token"
            )

        await add_to_blacklist(jti, exp)
        return success_response(data={}, message="Refresh token revoked successfully")

    except Exception as exc:
        return error_response(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Invalid refresh token",
            details=str(exc),
        )
