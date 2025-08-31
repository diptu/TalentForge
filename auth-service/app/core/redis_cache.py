# app/core/redis_cache.py
import redis.asyncio as redis

from app.core.config import settings

redis_client = redis.Redis(
    host=settings.redis.host,
    port=settings.redis.port,
    password=settings.redis.password,
    db=settings.redis.db,
    decode_responses=True,
)
