from fastapi.testclient import TestClient

from app.main import app


def test_root_status() -> None:
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"


def test_live_probe() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
