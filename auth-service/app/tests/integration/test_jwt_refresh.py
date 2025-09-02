# app/tests/integration/test_jwt_refresh.py

import pytest
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8001"


@pytest.mark.asyncio
async def test_refresh_token_flow() -> None:
    async with AsyncClient(base_url=BASE_URL) as client:
        # Step 1: Register a new user
        register_data = {
            "email": "refresh@example.com",
            "password": "StrongPassword$123",
        }
        resp = await client.post("/api/v1/auth/register", json=register_data)
        assert resp.status_code in (201, 400)  # 400 if user already exists

        # Step 2: Login to get access & refresh tokens
        login_data = {
            "email": "refresh@example.com",
            "password": "StrongPassword$123",
        }
        resp = await client.post("/api/v1/auth/login", json=login_data)
        assert resp.status_code == 200
        tokens = resp.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        assert access_token
        assert refresh_token

        # Step 3: Use refresh token to get new access token
        refresh_data = {"refresh_token": refresh_token}
        resp = await client.post("/api/v1/auth/refresh", json=refresh_data)
        assert resp.status_code == 200
        new_tokens = resp.json()
        new_access_token = new_tokens["access_token"]
        assert new_access_token
        assert new_tokens["token_type"] == "bearer"
