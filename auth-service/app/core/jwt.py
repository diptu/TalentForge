from datetime import datetime, timedelta

from jose import jwt

from app.core.config import settings


def create_access_token(data: dict) -> str:
    """
    Generate a JWT access token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt.access_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm
    )
    return encoded_jwt
