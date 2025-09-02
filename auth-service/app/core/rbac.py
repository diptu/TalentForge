# app/core/rbac.py
from __future__ import annotations

from typing import Dict, Optional, Sequence, TypedDict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token
from app.db.models import UserRole

# Use HTTPBearer for Authorization: Bearer <token>
bearer_scheme = HTTPBearer(auto_error=True)


class JWTPayload(TypedDict, total=False):
    """Shape of the JWT payload we expect/emit."""

    role: str  # "user" | "admin"
    email: str  # user's email
    iat: int
    exp: int
    jti: str


def require_roles(allowed_roles: Optional[Sequence[UserRole]] = None):
    """
    Dependency factory to enforce RBAC using JWT Bearer tokens.

    Parameters
    ----------
    allowed_roles : Optional[Sequence[UserRole]]
        Roles allowed to access the endpoint. If None, any authenticated user.

    Returns
    -------
    Callable[..., JWTPayload]
        A dependency that returns the validated JWT payload.
    """

    async def dependency(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    ) -> JWTPayload:
        token: str = credentials.credentials
        try:
            payload_dict: Dict[str, object] = decode_token(token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        # Normalize and type-check payload
        payload: JWTPayload = {}

        # role may be str or enum value at mint time → normalize to str
        role_val = payload_dict.get("role")
        if isinstance(role_val, UserRole):
            role_str = role_val.value
        elif isinstance(role_val, str):
            role_str = role_val
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Role information missing from token",
            )
        payload["role"] = role_str

        # required email
        email_val = payload_dict.get("email")
        if not isinstance(email_val, str):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email information missing from token",
            )
        payload["email"] = email_val

        if allowed_roles:
            allowed_str = {r.value for r in allowed_roles}
            if role_str not in allowed_str:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this resource",
                )

        # Copy through standard JWT timestamps if present and ints
        for k in ("iat", "exp"):
            v = payload_dict.get(k)
            if isinstance(v, int):
                payload[k] = v

        # jti is optional
        jti_val = payload_dict.get("jti")
        if isinstance(jti_val, str):
            payload["jti"] = jti_val

        return payload

    return dependency
