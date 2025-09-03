"""
File: app/api/v1/admin/schemas.py
Pydantic schemas for admin endpoints.
"""

from pydantic import BaseModel, EmailStr, Field


class AdminDashboardResponse(BaseModel):
    """Response schema for admin dashboard."""

    message: str = Field(..., description="Welcome message for the admin")


class AdminUserDataResponse(BaseModel):
    """User data schema returned to admin or user."""

    email: EmailStr = Field(..., description="User's email")
    role: str = Field(..., description="User's role")


class AdminUserDataEnvelope(BaseModel):
    """Envelope for user data response."""

    user: AdminUserDataResponse
    message: str = Field(..., description="Response message")
