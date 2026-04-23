from fastapi.testclient import TestClient

import src.modules.accent_cards as accent_cards
from src.server import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"server": "running"}


def test_module_endpoint():
    response = client.get(accent_cards.prefix)

    assert response.status_code == 200
    assert response.json() == {
        "module": accent_cards.module_name,
        "description": accent_cards.description,
        "version": accent_cards.version,
    }
