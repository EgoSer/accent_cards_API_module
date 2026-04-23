from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from src.core.sql.dependencies import get_async_session

from .meta import description, module_name, module_tags, prefix, version
from .models import Card
from .schemas import CardResponse

router = APIRouter(prefix=prefix, tags=module_tags)


@router.get("/")
def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"module": module_name, "description": description, "version": version}
    )


@router.get("/get_cards", response_model=dict[str, list[CardResponse]])
async def get_cards(
    amount: Annotated[
        int,
        Query(description="Returns less if amount of entries is less than desired amount"),
    ],
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Card).order_by(func.random()).limit(amount)
    cards = (await session.execute(query)).scalars().all()
    return {"cards": cards}
