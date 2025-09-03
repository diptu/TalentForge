"""
File: app/api/v1/auth/schemas.py
Pydantic schemas for authentication endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class TokenRefreshRequest(BaseModel):
    """Request schema for refreshing an access token."""

    refresh_token: str = Field(..., description="Valid refresh token")


class TokenLogoutRequest(BaseModel):
    """Request schema for logging out (revoking refresh token)."""

    refresh_token: str = Field(..., description="Refresh token to revoke")


class AuthTokensResponse(BaseModel):
    """Response schema for login and refresh endpoints."""

    access_token: str = Field(..., description="JWT access token")
    refresh_token: str | None = Field(
        None, description="JWT refresh token (login only)"
    )
    token_type: str = Field(default="bearer", description="Token type")
    role: str = Field(..., description="User role")
    email: EmailStr = Field(..., description="User email")


class RegisterResponse(BaseModel):
    """Response schema for user registration."""

    message: str = Field(..., description="Response message")
    user_id: int = Field(..., description="Newly created user ID")
    role: str = Field(..., description="Assigned user role")
