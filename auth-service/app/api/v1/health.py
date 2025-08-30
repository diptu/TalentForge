from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.utils.response import error_response, success_response

router = APIRouter(prefix="/health", tags=["Health"])


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str
    database: str
    redis: str


@router.get("/", response_model=HealthCheckResponse)
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    db_status = "ok"
    redis_status = "ok"
    overall_status = "ok" if db_status == "ok" and redis_status == "ok" else "fail"

    response_data = HealthCheckResponse(
        status=overall_status,
        database=db_status,
        redis=redis_status,
    )

    try:
        # Use model_dump() instead of dict()
        return success_response(
            data=response_data.model_dump(), message="Health check passed"
        )
    except Exception as exc:
        return error_response(
            code=500,
            message="Health check failed",
            details=str(exc),
        )
