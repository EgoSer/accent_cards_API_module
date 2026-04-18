from typing import Annotated

from fastapi import APIRouter, Query

from .meta import module_name, module_tags, prefix, version

router = APIRouter(prefix=prefix, tags=module_tags)


@router.get("/")
def root():
    return {"module": module_name, "version": version}


@router.get("/get_cards")
def get_cards(cards_number: Annotated[int, Query()]):
    pass
