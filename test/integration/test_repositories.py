import asyncio
from functools import wraps

from sqlalchemy import select

from src.modules.accent_cards.models import Card


def run_synchronous(async_function):
    @wraps(async_function)
    async def wrapper(*args, **kwargs):
        asyncio.get_event_loop().run_until_complete(async_function(*args, **kwargs))

    return wrapper


@run_synchronous
async def test_create_card(db_session):
    new_card = Card(word="торты", accent=2)

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card is not None


@run_synchronous
async def test_read_card(db_session):
    # Create card
    new_card = Card(word="торты", accent=2)

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card is not None

    # Read card
    query = select(Card).where(Card.id == new_card.id)
    card = (await db_session.execute(query)).scalar_one_or_none()

    assert card is not None
    assert card.id == new_card.id
    assert card.word == "торты"
    assert card.accent == 2


@run_synchronous
async def test_update_card(db_session):
    # Create card
    new_card = Card(word="торты", accent=2)

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card is not None

    # Update card fields
    query = select(Card).where(Card.id == new_card.id)
    card = (await db_session.execute(query)).scalar_one_or_none()

    assert card is not None

    card.word = "туфля"
    card.accent = 1
    await db_session.flush()
    await db_session.refresh(card)

    # Read again
    query = select(Card).where(Card.id == new_card.id)
    card = (await db_session.execute(query)).scalar_one_or_none()

    assert card is not None
    assert card.word == "туфля"
    assert card.accent == 1


@run_synchronous
async def test_delete_card(db_session):
    # Create card
    new_card = Card(word="торты", accent=2)

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card.id is not None

    query = select(Card).where(Card.id == new_card.id)
    card = (await db_session.execute(query)).scalar_one_or_none()

    assert card is not None

    db_session.delete(card)
    await db_session.flush()

    query = select(Card).where(Card.id == new_card.id)
    card = (await db_session.execute(query)).scalar_one_or_none()

    assert card is None
