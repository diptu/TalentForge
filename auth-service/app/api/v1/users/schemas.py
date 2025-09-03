"""
File: app/api/v1/users/schemas.py
Pydantic schemas for user-related endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class UserDataResponse(BaseModel):
    """Response schema for user data endpoint."""

    email: EmailStr = Field(..., description="Email address of the user")
    role: str = Field(..., description="Role assigned to the user")


class UserDataEnvelope(BaseModel):
    """Envelope response for /user-data endpoint."""

    user: UserDataResponse
    message: str = Field(..., description="Response message")


class UserProfileResponse(BaseModel):
    """Response schema for user profile endpoint."""

    email: EmailStr = Field(..., description="Email address of the user")
    role: str = Field(..., description="Role assigned to the user")
    issued_at: int | None = Field(
        None, description="JWT issued-at timestamp (Unix epoch)"
    )
    expires_at: int | None = Field(
        None, description="JWT expiration timestamp (Unix epoch)"
    )
