from fastapi.testclient import TestClient

from src.modules.accent_cards.meta import module_name as accent_module_name
from src.modules.accent_cards.meta import prefix as accent_prefix
from src.modules.accent_cards.meta import version as accent_version
from src.server import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"server": "running"}


def test_module_endpoint():
    response = client.get(accent_prefix)

    assert response.status_code == 200
    assert response.json() == {"module": accent_module_name, "version": accent_version}
