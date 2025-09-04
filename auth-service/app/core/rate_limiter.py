# app/core/rate_limiter.py

"""
app/core/rate_limiter.py

Implements rate limiting (fixed window) using Redis for FastAPI endpoints.
Prevents brute-force attacks and request flooding by IP or user identifier.
"""

from typing import Optional

import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, Request, status

from app.core.config import settings


class RateLimiter:
    """
    Fixed-window rate limiter backed by Redis.

    Parameters
    ----------
    redis_url : str
        Redis connection string.
    limit : int
        Maximum allowed requests in the window.
    window : int
        Time window in seconds.
    """

    def __init__(self, redis_url: str, limit: int, window: int) -> None:
        self.limit = limit
        self.window = window
        self.redis = aioredis.from_url(redis_url, decode_responses=True)

    async def check(
        self,
        request: Request,
        identifier: Optional[str] = None,
    ) -> None:
        """
        Check if request exceeds the allowed rate.

        Parameters
        ----------
        request : Request
            FastAPI request instance.
        identifier : str, optional
            Custom identifier (e.g., user_id). Defaults to client IP.
            When provided, a combination of IP + identifier is used.

        Raises
        ------
        HTTPException
            If request limit exceeded.
        """
        client_ip = request.client.host
        if identifier:
            key_id = f"user:{identifier}:ip:{client_ip}"
        else:
            key_id = f"ip:{client_ip}"

        endpoint = request.url.path
        key = f"rl:{endpoint}:{key_id}"

        current_count = await self.redis.incr(key)
        if current_count == 1:
            await self.redis.expire(key, self.window)

        if current_count > self.limit:
            ttl = await self.redis.ttl(key)
            retry_after = max(ttl, 1)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
                headers={"Retry-After": str(retry_after)},
            )


def get_rate_limiter() -> RateLimiter:
    """
    Dependency factory for rate limiter.

    Returns
    -------
    RateLimiter
        Configured rate limiter instance using settings.
    """
    redis_url = (
        f"redis://:{settings.redis.password}@{settings.redis.host}:"
        f"{settings.redis.port}/{settings.redis.db}"
    )
    return RateLimiter(
        redis_url=redis_url,
        limit=settings.rate_limit.count,
        window=settings.rate_limit.window,
    )


async def rate_limit_dependency(
    request: Request,
    limiter: RateLimiter = Depends(get_rate_limiter),
    user_id: Optional[str] = None,
) -> None:
    """
    FastAPI dependency for rate limiting.

    Parameters
    ----------
    request : Request
        FastAPI request instance.
    limiter : RateLimiter
        Rate limiter dependency.
    user_id : str, optional
        User identifier for combined IP + user rate limiting.

    Raises
    ------
    HTTPException
        If limit exceeded.
    """
    await limiter.check(request, identifier=user_id)
