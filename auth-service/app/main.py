# app/main.py

"""
File: app/main.py
FastAPI entrypoint for Auth Service with detailed OpenAPI documentation.
"""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.core.middleware import JWTBlacklistMiddleware
from app.api.v1 import api_v1_router


app = FastAPI(
    title="Auth Service",
    description=(
        "Authentication and user management service for the Job Board "
        "platform. Provides JWT-based authentication, refresh token "
        "rotation with revocation, and role-based access control (RBAC)."
    ),
    version="1.0.0",
    contact={
        "name": "Job Board Dev Team",
        "url": "https://jobboard.example.com",
        "email": "diptunazmulalam@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "auth",
            "description": (
                "Authentication operations including login, logout, and token refresh."
            ),
        },
        {
            "name": "users",
            "description": (
                "User management operations. Includes user creation, "
                "retrieval, updates, and deletion. Some endpoints require "
                "admin role."
            ),
        },
        {
            "name": "health",
            "description": "Service health check and metadata endpoints.",
        },
    ],
)


def custom_openapi() -> dict:
    """Customize OpenAPI schema with JWT Bearer security scheme."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": ("Enter the access token in the format: **Bearer <token>**"),
        }
    }

    # Apply BearerAuth security globally, unless overridden in endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override OpenAPI schema with custom version
app.openapi = custom_openapi

# Add middleware for token revocation checks
app.add_middleware(JWTBlacklistMiddleware)

# Include API v1 routers
app.include_router(api_v1_router, prefix="/api/v1")
