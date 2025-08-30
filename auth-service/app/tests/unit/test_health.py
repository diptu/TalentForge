from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    json_data = response.json()
    # Top-level status should be "success"
    assert json_data["status"] == "success"
    # Check actual health data inside `data`
    assert json_data["data"]["status"] == "ok"
    assert json_data["data"]["database"] == "ok"
    assert json_data["data"]["redis"] == "ok"
