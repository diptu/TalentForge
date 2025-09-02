# app/api/v1/users.py
from fastapi import APIRouter, Depends
from app.core.rbac import require_roles
from app.db.models import UserRole

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/user-data")
async def user_data(
    current_user: dict = Depends(require_roles([UserRole.USER, UserRole.ADMIN])),
):
    """
    Endpoint accessible by users or admins to view their own data.
    Returns email and role from JWT payload.
    """
    return {
        "user": {"email": current_user["email"], "role": current_user["role"]},
        "message": "User data retrieved successfully",
    }


@router.get("/profile")
async def user_profile(
    current_user: dict = Depends(require_roles([UserRole.USER, UserRole.ADMIN])),
):
    """
    Example profile endpoint for users or admins.
    Returns email, role, and token timestamps.
    """
    return {
        "email": current_user["email"],
        "role": current_user["role"],
        "issued_at": current_user.get("iat"),
        "expires_at": current_user.get("exp"),
    }
