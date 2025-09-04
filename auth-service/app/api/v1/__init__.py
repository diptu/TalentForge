# app/V1/__init__.py
"""
API v1 router aggregator.
"""

from fastapi import APIRouter

from .admin import router as admin_router
from .auth import router as auth_router
from .health import router as health_router
from .users import router as users_router

api_v1_router = APIRouter()

# Include all routers
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(admin_router)
api_v1_router.include_router(users_router)
