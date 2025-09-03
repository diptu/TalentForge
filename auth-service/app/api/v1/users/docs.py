"""
File: app/api/v1/users/docs.py
OpenAPI documentation metadata for user endpoints.
"""

from fastapi import status

USER_DATA_DOCS = {
    "summary": "Get user data",
    "description": (
        "Accessible by both **users** and **admins**. "
        "Returns the email and role of the authenticated user."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "User data retrieved successfully"},
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Invalid or missing token"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - Insufficient role permissions"
        },
    },
}

USER_PROFILE_DOCS = {
    "summary": "Get user profile",
    "description": (
        "Accessible by both **users** and **admins**. "
        "Returns email, role, and JWT token timestamps."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "Profile data retrieved"},
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized - Invalid or missing token"
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden - Insufficient role permissions"
        },
    },
}
