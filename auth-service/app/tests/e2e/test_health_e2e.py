# app/tests/e2e/test_health_e2e.py
import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_full_health() -> None:
    """Test the full system health endpoint.

    Sends a GET request to `/api/v1/health/` and verifies the
    structure and status of the response.

    Checks that the response contains keys for:
    - server
    - database
    - redis

    Also asserts that the overall status is either "ok" or "fail".
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/health/")
        assert response.status_code == 200, "Expected HTTP 200 OK"

        data = response.json()
        details = data.get("data", {}).get("details", {})
        assert "server" in details, "'server' key missing in response details"
        assert "database" in details, "'database' key missing in response details"
        assert "redis" in details, "'redis' key missing in response details"
        assert data["data"]["status"] in ("ok", "fail"), (
            "Status should be 'ok' or 'fail'"
        )
