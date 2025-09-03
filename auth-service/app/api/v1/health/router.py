"""
File: app/api/v1/health/router.py
Health check endpoints for server, database, and Redis.
"""

from typing import Any, Callable, Dict
from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_cache import redis_client
from app.db.session import get_db
from app.utils.response import success_response, error_response
from .schemas import HealthCheckResponse
from .docs import (
    SERVER_HEALTH_DOCS,
    DATABASE_HEALTH_DOCS,
    REDIS_HEALTH_DOCS,
    FULL_HEALTH_DOCS,
)

router = APIRouter(prefix="/health", tags=["health"])


async def _check_health(
    service_name: str,
    check_fn: Callable[..., Any],
    details_key: str | None = None,
) -> Dict[str, Any]:
    """
    Generic helper to perform a health check on a given service.

    Parameters
    ----------
    service_name : str
        Name of the service being checked.
    check_fn : Callable[..., Any]
        Async function performing the check. Returns True if healthy.
    details_key : str | None
        Optional key to include in the details dict.

    Returns
    -------
    Dict[str, Any]
        Standardized success or error response.
    """
    try:
        healthy = await check_fn()
        status_val = "ok" if healthy else "fail"
        details = {details_key: status_val} if details_key else None
        return success_response(
            data={"status": status_val, "details": details},
            message=f"{service_name} health check passed"
            if healthy
            else f"{service_name} health check failed",
        )
    except Exception as exc:
        details = {details_key: "fail"} if details_key else None
        return error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{service_name} health check failed",
            details=str(exc),
        )


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
