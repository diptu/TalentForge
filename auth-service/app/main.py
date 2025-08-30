"""
FastAPI entrypoint for Auth Service.
"""

from fastapi import FastAPI

from app.api.v1 import api_v1_router

app = FastAPI(title="Auth Service")

# Include API v1 routers
app.include_router(api_v1_router, prefix="/api/v1")
