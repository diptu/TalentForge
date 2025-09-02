# app/core/token_blacklist.py
"""Redis-backed refresh token blacklist."""

import time
from redis.asyncio import Redis

from app.core.config import settings

# Create a Redis client (async)
redis = Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    decode_responses=True,  # store as str instead of bytes
)


async def add_to_blacklist(jti: str, exp: int) -> None:
    """
    Add token JTI to blacklist until it expires.
    - jti: unique token ID
    - exp: expiration timestamp (unix seconds)
    """
    ttl = exp - int(time.time())
    if ttl > 0:
        await redis.setex(f"bl:{jti}", ttl, "revoked")


async def is_blacklisted(jti: str) -> bool:
    """
    Check if a token JTI is blacklisted.
    """
    return await redis.exists(f"bl:{jti}") == 1
