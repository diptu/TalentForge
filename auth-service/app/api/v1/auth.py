from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.hashing import hash_password, verify_password
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.services.token_blacklist import add_to_blacklist, is_blacklisted
from app.db import crud
from app.db.models import User, UserRole
from app.db.schemas import UserCreate, UserLogin
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenLogoutRequest(BaseModel):
    refresh_token: str


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
    role: Optional[UserRole] = UserRole.USER,
) -> Dict[str, Any]:
    existing_user = await crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    hashed_pw = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_pw, role=role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {
        "message": "User registered",
        "user_id": new_user.id,
        "role": new_user.role.value,
    }


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    db_user = await crud.get_user_by_email(db, user.email)
    if not db_user or not isinstance(db_user.hashed_password, str):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(email=db_user.email, role=db_user.role.value)
    refresh_token, jti = create_refresh_token(
        email=db_user.email, role=db_user.role.value
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": db_user.role.value,
        "email": db_user.email,
    }


@router.post("/refresh")
async def refresh_token(token_request: TokenRefreshRequest) -> Dict[str, Any]:
    payload = decode_token(token_request.refresh_token)
    jti: str = payload.get("jti", "")
    if jti and await is_blacklisted(jti):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    email: str = payload.get("email", "")
    role: str = payload.get("role", "user")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    new_access_token = create_access_token(email=email, role=role)
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "role": role,
        "email": email,
    }


@router.post("/logout")
async def logout(token_request: TokenLogoutRequest) -> Dict[str, Any]:
    try:
        payload = decode_token(token_request.refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    jti: str = payload.get("jti")
    exp: int = payload.get("exp", 0)
    if not jti or not exp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed refresh token"
        )

    await add_to_blacklist(jti, exp)
    return {"message": "Refresh token revoked successfully"}
