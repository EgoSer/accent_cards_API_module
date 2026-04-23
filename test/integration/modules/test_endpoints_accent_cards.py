import json
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from src.core.sql.dependencies import get_async_session
from src.modules.accent_cards.meta import prefix
from src.modules.accent_cards.models import Card
from src.server import app

client = TestClient(app)

# СУКА ПЕРЕДАВАТЬ В Depends НАДО ГЕНЕРАТОР AsyncGenerator[AsyncSession, None], А НЕ session_maker!!!!!!!!!!!!!


@pytest_asyncio.fixture(scope="function", loop_scope="function")
async def async_client(db_session) -> AsyncGenerator[AsyncClient]:
    def override_db_session():
        yield db_session

    app.dependency_overrides[get_async_session] = override_db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def accent_keywords():
    return [("торты", 1), ("туфля", 1), ("штаны", 4), ("машина", 3), ("ёжики", 0), ("двухъядерный", 5)]


@pytest.mark.asyncio
async def test_get_cards_endpoint_no_cards(async_client):
    amount = 10
    print(f"{prefix}/get_cards?amount={amount}")
    response = await async_client.get(f"{prefix}/get_cards?amount={amount}")

    assert response.status_code == 200
    assert response.json() == json.dumps({"cards": []})


@pytest.mark.asyncio
async def test_create_cards(db_session, accent_keywords):
    cards = [Card(word=word, accent=accent) for word, accent in accent_keywords]

    db_session.add_all(cards)
    await db_session.commit()

    assert cards is not None


def test_get_cards_endpoint_less_cards(accent_keywords, db_session):
    app.dependency_overrides[get_async_session] = db_session
    amount = 10
    response = client.get(f"{prefix}/get_cards?amount={amount}")
    app.dependency_overrides.clear()

    result = {word for word, _, _ in json.loads(response.json())["cards"].items()}

    for word, _ in accent_keywords:
        assert word in result


def test_get_cards_endpoint_more_cards(accent_keywords, db_session):
    app.dependency_overrides[get_async_session] = db_session
    amount = 2
    response = client.get(f"{prefix}/get_cards?amount={amount}")
    app.dependency_overrides.clear()

    assert response.status_code == 200

    result = {word: accent for word, accent, _ in json.loads(response.json())["cards"].items()}

    for word, accent in result.items():
        assert (word, accent) in accent_keywords
