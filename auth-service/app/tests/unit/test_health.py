import pytest
from fastapi.responses import JSONResponse

from app.api.v1.health import _check_health


@pytest.mark.asyncio
async def test_check_health_success():
    async def dummy_ok():
        return True

    response: JSONResponse = await _check_health("DummyService", dummy_ok)
    data = response.body.decode()
    assert "DummyService health check passed" in data
    assert '"status":"ok"' in data


@pytest.mark.asyncio
async def test_check_health_failure():
    async def dummy_fail():
        return False

    response: JSONResponse = await _check_health("DummyService", dummy_fail)
    data = response.body.decode()
    assert "DummyService health check failed" in data
    assert '"status":"fail"' in data
