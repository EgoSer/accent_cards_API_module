import json

import pytest
from fastapi.testclient import TestClient

from src.modules.accent_cards.meta import prefix
from src.modules.accent_cards.models import Card
from src.server import app

client = TestClient(app)


@pytest.fixture(scope="module")
def accent_keywords():
    return [("торты", 1), ("туфля", 1), ("штаны", 4), ("машина", 3), ("ёжики", 0), ("двухядерный", 4)]


def test_get_cards_endpoint_no_cards():
    amount = 10
    response = client.get(f"{prefix}/get_cards?amount={amount}")

    assert response.status_code == 200
    assert response.json() == json.dumps({"cards": []})


@pytest.mark.asyncio
async def test_create_cards(db_session, accent_keywords):
    cards = [Card(word=word, accent=accent) for word, accent in accent_keywords]

    db_session.add(cards)
    await db_session.commit()

    assert cards is not None


def test_get_cards_endpoint_less_cards(accent_keywords):
    amount = 10
    response = client.get(f"{prefix}/get_cards?amount={amount}")

    assert response.status_code == 200

    result = {word for word, _, _ in json.loads(response.json())["cards"].items()}

    for word, _ in accent_keywords:
        assert word in result


def test_get_cards_endpoint_more_cards(accent_keywords):
    amount = 2
    response = client.get(f"{prefix}/get_cards?amount={amount}")

    assert response.status_code == 200

    result = {word: accent for word, accent, _ in json.loads(response.json())["cards"].items()}

    for word, accent in result.items():
        assert (word, accent) in accent_keywords
