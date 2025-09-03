"""
File: app/api/v1/health/schemas.py
Pydantic schemas for health check responses.
"""

from typing import Any, Dict
from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """Schema representing the health check response."""

    status: str = Field(..., description="Overall status (ok or fail)")
    details: Dict[str, Any] | None = Field(
        None, description="Detailed sub-service health information"
    )
