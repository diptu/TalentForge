"""
File: app/utils/response.py
Standardized JSON response helpers for API endpoints.
"""

from typing import Any, Dict

from fastapi import status
from fastapi.responses import JSONResponse


def success_response(data: Any, message: str = "Success") -> JSONResponse:
    """
    Standardized JSON response for successful API calls.

    Parameters
    ----------
    data : Any
        The payload data to include in the response.
    message : str, optional
        Human-readable message (default "Success").

    Returns
    -------
    JSONResponse
        FastAPI JSONResponse with structured success format.
    """
    response_content: Dict[str, Any] = {
        "status": "success",
        "message": message,
        "data": data,
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=response_content)


def error_response(code: int, message: str, details: Any = None) -> JSONResponse:
    """
    Standardized JSON response for API errors.

    Parameters
    ----------
    code : int
        HTTP status code to return.
    message : str
        Human-readable error message.
    details : Any, optional
        Optional additional information about the error.

    Returns
    -------
    JSONResponse
        FastAPI JSONResponse with structured error format.
    """
    response_content: Dict[str, Any] = {"status": "error", "message": message}
    if details is not None:
        response_content["details"] = details
    return JSONResponse(status_code=code, content=response_content)
