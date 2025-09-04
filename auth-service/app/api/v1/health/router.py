from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_cache import redis_client
from app.db.session import get_db
from app.utils.response import success_response

from .docs import (
    DATABASE_HEALTH_DOCS,
    FULL_HEALTH_DOCS,
    REDIS_HEALTH_DOCS,
    SERVER_HEALTH_DOCS,
)
from .schemas import HealthCheckResponse
from .utils import check_health as _check_health  # Updated import

# --- endpoints remain the same ---

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/server", response_model=HealthCheckResponse, **SERVER_HEALTH_DOCS)
async def server_health() -> Dict[str, Any]:
    """Liveness check for the API server."""

    async def server_check() -> bool:
        return True

    return await _check_health("Server", server_check, details_key="server")


@router.get("/database", response_model=HealthCheckResponse, **DATABASE_HEALTH_DOCS)
async def database_health(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Check database connectivity."""

    async def db_check() -> bool:
        await db.execute(text("SELECT 1"))
        return True

    return await _check_health("Database", db_check, details_key="database")


@router.get("/redis", response_model=HealthCheckResponse, **REDIS_HEALTH_DOCS)
async def redis_health() -> Dict[str, Any]:
    """Check Redis connectivity."""

    async def redis_check() -> bool:
        pong = await redis_client.ping()
        return bool(pong)

    return await _check_health("Redis", redis_check, details_key="redis")


@router.get("/", response_model=HealthCheckResponse, **FULL_HEALTH_DOCS)
async def full_health(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """Combined system health check for server, database, and Redis."""
    results: Dict[str, str] = {"server": "ok"}

    try:
        await db.execute(text("SELECT 1"))
        results["database"] = "ok"
    except Exception:
        results["database"] = "fail"

    try:
        pong = await redis_client.ping()
        results["redis"] = "ok" if pong else "fail"
    except Exception:
        results["redis"] = "fail"

    overall_status = "ok" if all(val == "ok" for val in results.values()) else "fail"
    return success_response(
        data={"status": overall_status, "details": results},
        message="Full system health check completed",
    )
