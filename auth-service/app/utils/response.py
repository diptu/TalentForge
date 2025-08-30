"""
Response utility module for standardized API responses.

Provides helper functions to format success and error responses
consistently across the application.
"""

from typing import Any, Optional

from fastapi.responses import JSONResponse


def success_response(
    data: Any = None, code: int = 200, message: str = "Success"
) -> JSONResponse:
    """
    Create a standardized success response.

    Parameters
    ----------
    data : Any, optional
        The response payload, by default None
    code : int, optional
        HTTP status code, by default 200
    message : str, optional
        Human-readable success message, by default "Success"

    Returns
    -------
    JSONResponse
        A FastAPI JSONResponse with the standardized structure.

    Example
    -------
    >>> success_response(data={"id": 1}, message="User created")
    JSONResponse(content={'status': 'success', 'code': 200,
                          'message': 'User created', 'data': {'id': 1}})
    """
    return JSONResponse(
        status_code=code,
        content={
            "status": "success",
            "code": code,
            "message": message,
            "data": data,
        },
    )


def error_response(
    code: int = 400, message: str = "Error", details: Optional[Any] = None
) -> JSONResponse:
    """
    Create a standardized error response.

    Parameters
    ----------
    code : int, optional
        HTTP status code, by default 400
    message : str, optional
        Human-readable error message, by default "Error"
    details : Any, optional
        Additional error details, by default None

    Returns
    -------
    JSONResponse
        A FastAPI JSONResponse with the standardized error structure.

    Example
    -------
    >>> error_response(code=404, message="Not Found", details="User not found")
    JSONResponse(content={'status': 'error', 'code': 404,
                          'message': 'Not Found', 'details': 'User not found'})
    """
    return JSONResponse(
        status_code=code,
        content={
            "status": "error",
            "code": code,
            "message": message,
            "details": details,
        },
    )
