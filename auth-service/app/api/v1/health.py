"""Health check endpoints for the API.

This module provides endpoints to verify the health of the server,
database, and Redis cache. Includes individual checks and a combined
endpoint for full system health.
"""

from typing import Any, Callable, Dict

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis_cache import redis_client
from app.db.session import get_db
from app.utils.response import error_response, success_response

router = APIRouter(prefix="/health", tags=["Health"])


class HealthCheckResponse(BaseModel):
    """Model representing the health check response.

    Attributes
    ----------
    status : str
        Overall status of the service ('ok' or 'fail').
    details : dict, optional
        Optional dictionary with more detailed information about sub-services.
    """

    status: str
    details: Dict[str, Any] | None = None


async def _check_health(
    service_name: str,
    check_fn: Callable[..., Any],
    details_key: str | None = None,
) -> JSONResponse:
    """Generic helper to perform a health check on a given service.

    Parameters
    ----------
    service_name : str
        Name of the service being checked (used in messages).
    check_fn : Callable[..., Any]
        Async function performing the actual check. Should return True if healthy.
    details_key : str | None
        Optional key to include in the details dictionary.

    Returns
    -------
    JSONResponse
        Standardized JSON response indicating service health.
    """
    try:
        healthy = await check_fn()
        status = "ok" if healthy else "fail"
        details = {details_key: status} if details_key else None
        response = HealthCheckResponse(status=status, details=details)
        return success_response(
            data=response.model_dump(),
            message=(
                f"{service_name} health check passed"
                if healthy
                else f"{service_name} health check failed"
            ),
        )
    except Exception as exc:
        details = {details_key: "fail"} if details_key else None
        response = HealthCheckResponse(status="fail", details=details)
        return error_response(
            code=500,
            message=f"{service_name} health check failed",
            details=str(exc),
        )


@router.get("/server", response_model=HealthCheckResponse)
async def server_health() -> JSONResponse:
    """Check server liveness.

    Returns
    -------
    JSONResponse
        Status of the API server.
    """

    async def check() -> bool:
        return True

    return await _check_health("Server", check, details_key="server")


@router.get("/database", response_model=HealthCheckResponse)
async def database_health(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Check database connectivity.

    Parameters
    ----------
    db : AsyncSession
        SQLAlchemy async session dependency.

    Returns
    -------
    JSONResponse
        Status of the database connection.
    """

    async def db_check() -> bool:
        await db.execute(text("SELECT 1"))
        return True

    return await _check_health("Database", db_check, details_key="database")


@router.get("/redis", response_model=HealthCheckResponse)
async def redis_health() -> JSONResponse:
    """Check Redis connectivity.

    Returns
    -------
    JSONResponse
        Status of the Redis connection.
    """

    async def redis_check() -> bool:
        pong = await redis_client.ping()
        return bool(pong)

    return await _check_health("Redis", redis_check, details_key="redis")


@router.get("/", response_model=HealthCheckResponse)
async def full_health(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """Check full system health (server, database, Redis).

    Parameters
    ----------
    db : AsyncSession
        SQLAlchemy async session dependency.

    Returns
    -------
    JSONResponse
        Combined health status with details per service.
    """
    results: Dict[str, str] = {}

    # Server check
    results["server"] = "ok"

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        results["database"] = "ok"
    except Exception:
        results["database"] = "fail"

    # Redis check
    try:
        pong = await redis_client.ping()
        results["redis"] = "ok" if pong else "fail"
    except Exception:
        results["redis"] = "fail"

    overall_status = (
        "ok" if all(status == "ok" for status in results.values()) else "fail"
    )
    response = HealthCheckResponse(status=overall_status, details=results)
    return success_response(
        data=response.model_dump(),
        message="Full system health check completed",
    )
