# app/tests/integration/test_health_endpoints.py
from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.db.session import AsyncSession, get_db  # <- import get_db here
from app.main import app


@pytest.mark.asyncio
async def test_database_health_ok():
    """Test database health endpoint returns ok with a mocked AsyncSession."""

    # Create a mock AsyncSession
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = AsyncMock()  # awaitable
    mock_session.begin.return_value.__aenter__.return_value = None
    mock_session.begin.return_value.__aexit__.return_value = None

    async def mock_get_db() -> None:
        """Async generator to mock get_db dependency."""
        yield mock_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Patch the dependency dynamically
        app.dependency_overrides[get_db] = mock_get_db

        response = await client.get("/api/v1/health/database")
        assert response.status_code == 200
        data = response.json()

        assert data["data"]["details"]["database"] == "ok"

        # Cleanup
        app.dependency_overrides.clear()
