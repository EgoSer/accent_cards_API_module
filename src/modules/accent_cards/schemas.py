import uuid
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

allowed_characters = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя")


class CardSchema(BaseModel):
    word: Annotated[
        str, Field(min_length=1, max_length=38, description="A word in lowercase without any trailing symbols")
    ]
    accent: Annotated[
        int, Field(gt=-1, description="A number of letter starting with 0 which points to true accented letter")
    ]

    @field_validator("word", mode="before")
    def word_field_validator(cls, value) -> str:
        if not isinstance(value, str):
            raise ValueError("Word must be a string")

        if not set(value).issubset(allowed_characters):
            raise ValueError("Word contains unallowed characters!")

        return value.lower().strip()

    @model_validator(mode="after")
    def word_validator(self) -> Self:
        if self.accent >= len(self.word):
            raise ValueError("Accent letter number cannot be greater than number of letters in word")
        return self

    model_config = ConfigDict(from_attributes=True)


class CardResponse(CardSchema):
    id: Annotated[uuid.UUID, Field()]
