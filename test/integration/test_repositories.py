import pytest
from sqlalchemy import select

from src.modules.accent_cards.models import Card


class TestAccentCardCRUD:
    """Test CRUD operations on Accent card model"""

    def __init__(self):
        self.card_id = None

    @pytest.mark.asyncio
    async def test_create_card(self, db_class_session):
        new_card = Card(word="торты", accent=2)

        db_class_session.add(new_card)
        await db_class_session.flush()
        await db_class_session.refresh(new_card)

        assert new_card.id is not None
        self.card_id = new_card.id

    @pytest.mark.asyncio
    async def test_read_card(self, db_class_session):
        query = select(Card).where(Card.word == "торты")
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None
        assert card.id == self.card_id
        assert card.word == "торты"
        assert card.accent == 2

    @pytest.mark.asyncio
    async def test_update_card(self, db_class_session):
        query = select(Card).where(Card.word == "торты")
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        card.word = "туфля"
        card.accent = 1
        await db_class_session.flush()
        await db_class_session.refresh(card)

        # Read again
        query = select(Card).where(Card.id == self.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None
        assert card.word == "туфля"
        assert card.accent == 1

    @pytest.mark.asyncio
    async def test_delete_card(self, db_class_session):
        query = select(Card).where(Card.id == self.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        db_class_session.delete(card)
        await db_class_session.flush()

        query = select(Card).where(Card.id == self.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is None
