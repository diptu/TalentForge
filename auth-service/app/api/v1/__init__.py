# app/V1/__init__.py
"""
API v1 router aggregator.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .health import router as health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
