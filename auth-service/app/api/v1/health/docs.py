"""
File: app/api/v1/health/docs.py
OpenAPI documentation for health endpoints.
"""

from fastapi import status

SERVER_HEALTH_DOCS = {
    "summary": "Server health",
    "description": "Check API server liveness.",
    "responses": {
        status.HTTP_200_OK: {"description": "Server is healthy"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server health check failed"
        },
    },
}

DATABASE_HEALTH_DOCS = {
    "summary": "Database health",
    "description": "Check PostgreSQL database connectivity.",
    "responses": {
        status.HTTP_200_OK: {"description": "Database is healthy"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Database health check failed"
        },
    },
}

REDIS_HEALTH_DOCS = {
    "summary": "Redis health",
    "description": "Check Redis cache connectivity.",
    "responses": {
        status.HTTP_200_OK: {"description": "Redis is healthy"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Redis health check failed"
        },
    },
}

FULL_HEALTH_DOCS = {
    "summary": "Full system health",
    "description": "Check server, database, and Redis in a combined response.",
    "responses": {
        status.HTTP_200_OK: {"description": "All services are healthy"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "One or more services are unhealthy"
        },
    },
}
