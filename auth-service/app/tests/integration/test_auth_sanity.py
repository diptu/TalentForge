import pytest
from httpx import AsyncClient

from app.main import app

BASE_URL = "http://testserver"

TEST_USER = {"email": "sanitytest@example.com", "password": "StrongPassword$123"}


@pytest.mark.asyncio
async def test_auth_sanity():
    async with AsyncClient(app=app, base_url=BASE_URL) as client:
        # 1️⃣ Register
        resp = await client.post("/api/v1/auth/register", json=TEST_USER)
        assert resp.status_code in (201, 400)  # 400 if already exists
        if resp.status_code == 201:
            data = resp.json()
            assert "user_id" in data
            assert data["role"] == "user"

        # 2️⃣ Login
        resp = await client.post("/api/v1/auth/login", json=TEST_USER)
        assert resp.status_code == 200
        tokens = resp.json()
        access_token = tokens["access_token"]
        refresh_token = tokens["refresh_token"]
        assert tokens["role"] == "user"

        headers = {"Authorization": f"Bearer {access_token}"}

        # 3️⃣ Access /user-data
        resp = await client.get("/api/v1/users/user-data", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == TEST_USER["email"]
        assert data["role"] == "user"

        # 4️⃣ Access /profile
        resp = await client.get("/api/v1/users/profile", headers=headers)
        assert resp.status_code == 200
        profile = resp.json()
        assert profile["email"] == TEST_USER["email"]
        assert profile["role"] == "user"

        # 5️⃣ Refresh token
        resp = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert resp.status_code == 200
        new_access_token = resp.json()["access_token"]
        assert new_access_token != access_token

        # 6️⃣ Logout (revoke refresh token)
        resp = await client.post(
            "/api/v1/auth/logout", json={"refresh_token": refresh_token}
        )
        assert resp.status_code == 200
        assert resp.json()["message"] == "Refresh token revoked successfully"

        # 7️⃣ Attempt refresh again (should fail)
        resp = await client.post(
            "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
        )
        assert resp.status_code == 401
        assert "revoked" in resp.json()["detail"].lower()
