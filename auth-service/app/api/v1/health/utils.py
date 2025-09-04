from typing import Any, Callable, Dict

from fastapi import status

from app.utils.response import error_response, success_response


async def check_health(
    service_name: str,
    check_fn: Callable[..., Any],
    details_key: str | None = None,
) -> Dict[str, Any]:
    """
    Generic helper to perform a health check on a given service.
    Returns a standardized success or error response.
    """
    try:
        healthy = await check_fn()
        status_val = "ok" if healthy else "fail"
        details = {details_key: status_val} if details_key else None
        return success_response(
            data={"status": status_val, "details": details},
            message=(
                f"{service_name} health check passed"
                if healthy
                else f"{service_name} health check failed"
            ),
        )
    except Exception as exc:
        details = {details_key: "fail"} if details_key else None
        return error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"{service_name} health check failed",
            details=str(exc),
        )
