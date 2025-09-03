"""
File: app/api/v1/admin/docs.py
OpenAPI documentation for admin endpoints.
"""

from fastapi import status

ADMIN_DASHBOARD_DOCS = {
    "summary": "Admin dashboard",
    "description": "Admin-only dashboard endpoint. Returns welcome message.",
    "responses": {
        status.HTTP_200_OK: {"description": "Dashboard message returned"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden - insufficient role"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized access"},
    },
}

ADMIN_USER_DATA_DOCS = {
    "summary": "Get user data",
    "description": (
        "Endpoint accessible by users or admins to view user information. "
        "Returns email and role."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "User data retrieved successfully"},
        status.HTTP_403_FORBIDDEN: {"description": "Forbidden - insufficient role"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Unauthorized access"},
    },
}
