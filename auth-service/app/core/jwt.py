"""
JWT utility functions for access and refresh token handling.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, cast
import jwt

from app.core.config import settings


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a short-lived access token.

    Parameters
    ----------
    data : dict
        The payload containing user information.

    Returns
    -------
    str
        Encoded JWT access token.
    """
    expire: datetime = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt.access_expire_minutes
    )
    payload: Dict[str, Any] = {**data, "exp": expire, "type": "access"}
    return str(
        jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    )


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create a long-lived refresh token.

    Parameters
    ----------
    data : dict
        The payload containing user information.

    Returns
    -------
    str
        Encoded JWT refresh token.
    """
    expire: datetime = datetime.now(timezone.utc) + timedelta(
        days=settings.jwt.refresh_expire_days
    )
    payload: Dict[str, Any] = {**data, "exp": expire, "type": "refresh"}
    return str(
        jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
    )


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and verify a JWT token.

    Parameters
    ----------
    token : str
        Encoded JWT token.

    Returns
    -------
    dict
        Decoded token payload.
    """
    payload = jwt.decode(
        token,
        settings.jwt.secret_key,
        algorithms=[settings.jwt.algorithm],
    )
    return cast(Dict[str, Any], payload)
