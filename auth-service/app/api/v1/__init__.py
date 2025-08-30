"""
API v1 router aggregator.
"""

from fastapi import APIRouter

from .health import router as health_router

api_v1_router = APIRouter()
api_v1_router.include_router(health_router)
