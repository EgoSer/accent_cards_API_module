import pytest
import pytest_asyncio
from loguru import logger
from sqlalchemy import select

from src.modules.accent_cards.models import Card


class TestAccentCardCRUD:
    """Test CRUD operations on Accent card model"""

    @pytest_asyncio.fixture(scope="class", loop_scope="class", autouse=True)
    async def setup_card(self, db_class_session):
        new_card = Card(word="торты", accent=2)

        db_class_session.add(new_card)
        await db_class_session.flush()
        await db_class_session.refresh(new_card)

        assert new_card.id is not None
        TestAccentCardCRUD.card_id = new_card.id
        logger.info(f"setup_card fixture: Created card: {new_card}")
        yield

    @pytest.mark.asyncio
    async def test_create_card(self, db_class_session):
        new_card = Card(word="машины", accent=4)

        db_class_session.add(new_card)
        await db_class_session.flush()
        await db_class_session.refresh(new_card)

        assert new_card.id is not None
        assert new_card.id != TestAccentCardCRUD.card_id
        logger.info(f"CREATE test: Created card: {new_card}")

    @pytest.mark.asyncio
    async def test_read_card(self, db_class_session):
        assert hasattr(self, "card_id")

        query = select(Card).where(Card.word == "торты")
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None

        logger.info(f"READ test: Found card: {card}")
        assert card.id == TestAccentCardCRUD.card_id
        assert card.word == "торты"
        assert card.accent == 2

    @pytest.mark.asyncio
    async def test_update_card(self, db_class_session):
        assert hasattr(self, "card_id")

        query = select(Card).where(Card.word == "торты")
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None
        logger.info(f"UPDATE test: Found card: {card}")

        card.word = "туфля"
        card.accent = 1
        await db_class_session.flush()
        await db_class_session.refresh(card)

        # Read again
        query = select(Card).where(Card.id == TestAccentCardCRUD.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None
        assert card.word == "туфля"
        assert card.accent == 1
        logger.info(f"UPDATE test: Modified card: {card}")

    @pytest.mark.asyncio
    async def test_delete_card(self, db_class_session):
        assert hasattr(self, "card_id")

        query = select(Card).where(Card.id == TestAccentCardCRUD.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is not None
        logger.info(f"DELETE test: Found card: {card}")

        db_class_session.delete(card)
        await db_class_session.flush()

        query = select(Card).where(Card.id == TestAccentCardCRUD.card_id)
        card = (await db_class_session.execute(query)).scalar_one_or_none()

        assert card is None
        logger.info("DELETE test: Deleted card")
