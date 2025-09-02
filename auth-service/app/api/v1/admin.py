# app/api/v1/admin.py
from fastapi import APIRouter, Depends
from app.core.rbac import require_roles
from app.db.models import UserRole

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard")
async def admin_dashboard(
    current_user: dict = Depends(require_roles([UserRole.ADMIN])),
):
    """
    Admin-only dashboard.
    Returns email and role from JWT payload.
    """
    return {
        "message": f"Welcome, admin {current_user['email']} with role {current_user['role']}"
    }


@router.get("/user-data")
async def user_data(
    current_user: dict = Depends(require_roles([UserRole.USER, UserRole.ADMIN])),
):
    """
    Endpoint accessible by users or admins to view their data.
    """
    return {
        "user": {"email": current_user["email"], "role": current_user["role"]},
        "message": "User data retrieved successfully",
    }
