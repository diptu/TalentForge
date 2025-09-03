"""
File: app/api/v1/users/__init__.py
Package entrypoint for user API.
"""

from .router import router

__all__ = ["router"]
