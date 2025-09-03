"""
File: app/api/v1/auth/docs.py
OpenAPI documentation metadata for authentication endpoints.
"""

from fastapi import status

REGISTER_DOCS = {
    "summary": "Register new user",
    "description": (
        "Registers a new user with email and password. "
        "Rate limited per IP to prevent abuse."
    ),
    "responses": {
        status.HTTP_201_CREATED: {"description": "User registered successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"},
        status.HTTP_429_TOO_MANY_REQUESTS: {"description": "Rate limit exceeded"},
    },
}

LOGIN_DOCS = {
    "summary": "User login",
    "description": (
        "Authenticates a user with email and password. "
        "Returns access and refresh tokens. "
        "Rate limited per IP + email to prevent brute force attacks."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "Login successful"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid credentials"},
        status.HTTP_429_TOO_MANY_REQUESTS: {"description": "Rate limit exceeded"},
    },
}

REFRESH_DOCS = {
    "summary": "Refresh access token",
    "description": (
        "Generates a new access token using a valid refresh token. "
        "Refresh tokens may be revoked (blacklisted)."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "Access token refreshed"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid or revoked token"},
    },
}

LOGOUT_DOCS = {
    "summary": "Logout (revoke refresh token)",
    "description": (
        "Invalidates a refresh token by adding it to the blacklist. "
        "Prevents further use of this token."
    ),
    "responses": {
        status.HTTP_200_OK: {"description": "Token revoked successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid refresh token"},
    },
}
