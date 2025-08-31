# app/tests/integration/test_health_endpoints.py
import pytest
from unittest.mock import AsyncMock
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app
from app.db.session import get_db, AsyncSession  # <- import get_db here


@pytest.mark.asyncio
async def test_database_health_ok():
    """Test database health endpoint returns ok with a mocked AsyncSession."""

    # Create a mock AsyncSession
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute.return_value = AsyncMock()  # awaitable
    mock_session.begin.return_value.__aenter__.return_value = None
    mock_session.begin.return_value.__aexit__.return_value = None

    async def mock_get_db():
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
