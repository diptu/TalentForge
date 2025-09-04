"""
File: app/api/v1/admin/router.py
Admin-related API routes with RBAC and OpenAPI docs.
"""

from typing import Any, Dict

from fastapi import APIRouter, Depends

from app.core.rbac import require_roles
from app.db.models import UserRole

from .docs import ADMIN_DASHBOARD_DOCS, ADMIN_USER_DATA_DOCS
from .schemas import AdminDashboardResponse, AdminUserDataEnvelope

# ⚠ router must be defined BEFORE using @router.get decorators
router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/dashboard", response_model=AdminDashboardResponse, **ADMIN_DASHBOARD_DOCS)
async def admin_dashboard(
    current_user: Dict[str, Any] = Depends(require_roles([UserRole.ADMIN])),
) -> Dict[str, Any]:
    """Admin-only dashboard endpoint."""
    message = f"Welcome, admin {current_user['email']} with role {current_user['role']}"
    return {"message": message}


@router.get("/user-data", response_model=AdminUserDataEnvelope, **ADMIN_USER_DATA_DOCS)
async def admin_user_data(
    current_user: Dict[str, Any] = Depends(
        require_roles([UserRole.USER, UserRole.ADMIN])
    ),
) -> Dict[str, Any]:
    """Endpoint accessible by users or admins to view their own data."""
    data = {"user": {"email": current_user["email"], "role": current_user["role"]}}
    return {"user": data["user"], "message": "User data retrieved successfully"}
