import pytest

from src.modules.accent_cards.models import Card
from src.modules.accent_cards.schemas import CardSchema


@pytest.mark.asyncio
async def test_schema_to_orm_convertation(db_session):
    card = CardSchema(word="Привет", accent=4)

    new_card = Card(**card.model_dump())

    db_session.add(new_card)
    await db_session.flush()
    await db_session.refresh(new_card)

    assert new_card.id is not None


def test_schema_accent_too_high():
    with pytest.raises(ValueError) as exc_info:
        card = CardSchema(word="Привет", accent=15)


def test_schema_accent_negative():
    with pytest.raises(ValueError) as exc_info:
        card = CardSchema(word="Привет", accent=-1)


def test_schema_word_too_short():
    with pytest.raises(ValueError) as exc_info:
        card = CardSchema(word="", accent=-1)


def test_schema_word_too_long():
    with pytest.raises(ValueError) as exc_info:
        card = CardSchema(word="выалопрдлыврапоыварпыврпрывапылврпыврлоплывап", accent=-1)


def test_schema_word_incorrect_format():
    with pytest.raises(ValueError) as exc_info:
        card = CardSchema(word="Привет, мир!", accent=2)
