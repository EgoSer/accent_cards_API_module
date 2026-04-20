import pytest
from sqlalchemy import select

from src.modules.accent_cards.models import Card


@pytest.mark.asyncio
async def test_crud_card(db_session):
    """Test CRUD operations on Accent card model"""
    # Create
    new_card = Card(word="торты", accent=2)

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card.id is not None

    # Read
    query = select(Card).where(Card.id == new_card.id)
    result = (await db_session.execute(query)).scalar_one_or_none()

    assert result is not None
    assert result.id == new_card.id
    assert result.word == "торты"
    assert result.accent == 2

    # Update
    result.word = "туфля"
    result.accent = 1
    await db_session.flush()
    await db_session.refresh(new_card)

    # Read (again)
    query = select(Card).where(Card.id == new_card.id)
    result = (await db_session.execute(query)).scalar_one_or_none()

    assert result is not None
    assert result.id == new_card.id
    assert result.word == "туфля"
    assert result.accent == 1

    # Delete
    db_session.delete(new_card)
    db_session.flush()

    query = select(Card).where(Card.id == new_card.id)
    result = (await db_session.execute(query)).scalar_one_or_none()

    assert result is None
