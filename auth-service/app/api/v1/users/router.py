"""
File: app/api/v1/users/router.py
User-related API routes with RBAC and OpenAPI docs.
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.rbac import require_roles
from app.db.models import UserRole
from app.utils.response import success_response

from .docs import USER_DATA_DOCS, USER_PROFILE_DOCS
from .schemas import UserDataEnvelope, UserProfileResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/user-data", response_model=UserDataEnvelope, **USER_DATA_DOCS)
async def user_data(
    current_user: Dict[str, Any] = Depends(
        require_roles([UserRole.USER, UserRole.ADMIN])
    ),
) -> Dict[str, Any]:
    """
    Retrieve the authenticated user's email and role.
    """
    data = {
        "user": {
            "email": current_user["email"],
            "role": current_user["role"],
        },
        "message": "User data retrieved successfully",
    }
    return success_response(data=data, message="User data retrieved successfully")


@router.get("/profile", response_model=UserProfileResponse, **USER_PROFILE_DOCS)
async def user_profile(
    current_user: Dict[str, Any] = Depends(
        require_roles([UserRole.USER, UserRole.ADMIN])
    ),
) -> Dict[str, Any]:
    """
    Retrieve user profile details including token metadata.
    """
    data = {
        "email": current_user["email"],
        "role": current_user["role"],
        "issued_at": current_user.get("iat"),
        "expires_at": current_user.get("exp"),
    }
    return success_response(data=data, message="Profile retrieved successfully")
