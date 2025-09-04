# app/core/security.py
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from app.core.config import settings

SECRET_KEY = settings.jwt.secret_key
ALGORITHM = settings.jwt.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.jwt.access_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS = settings.jwt.refresh_expire_days


def create_access_token(
    email: str, role: str, expires_delta: timedelta | None = None
) -> str:
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "email": email,
        "role": role,
        "iat": now,
        "exp": expire,
    }
    return str(jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM))


def create_refresh_token(
    email: str, role: str, expires_delta: timedelta | None = None
) -> tuple[str, str]:
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    jti = str(uuid.uuid4())
    payload = {
        "email": email,
        "role": role,
        "iat": now,
        "exp": expire,
        "jti": jti,
    }
    token = str(jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM))
    return token, jti


def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
