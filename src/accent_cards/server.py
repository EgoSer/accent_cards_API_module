from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
def root():
    return {"server": "running"}


@app.get("/cards")
def get_cards(cards_number: Annotated[int, Query()]):
    pass
