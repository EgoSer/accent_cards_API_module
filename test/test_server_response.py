from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"server": "running"}
