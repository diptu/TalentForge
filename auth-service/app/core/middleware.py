# app/core/middlewere.py

from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.security import decode_token
from app.services.token_blacklist import is_blacklisted


class JWTBlacklistMiddleware(BaseHTTPMiddleware):
    """
    Middleware to check if access or refresh token has been revoked.
    Assumes JWT is sent via Authorization header as Bearer token.
    """

    async def dispatch(self, request: Request, call_next):
        auth: HTTPAuthorizationCredentials = await HTTPBearer(auto_error=False)(request)
        if auth:
            token = auth.credentials
            try:
                payload = decode_token(token)
                jti = payload.get("jti")
                if jti and await is_blacklisted(jti):
                    raise HTTPException(
                        status_code=401, detail="Token has been revoked"
                    )
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid token")
        response = await call_next(request)
        return response
