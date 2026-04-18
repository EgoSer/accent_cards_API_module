import uuid
from typing import Annotated, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CardSchema(BaseModel):
    word: Annotated[str, Field(max_length=38, description="A word in lowercase without any trailing symbols")]
    accent: Annotated[int, Field(description="A number of letter starting with 0 which points to true accented letter")]

    @model_validator(mode="after")
    def word_validator(self) -> Self:
        if self.accent >= len(self.word):
            raise ValueError("Accent letter number cannot be greater than number of letters in word")
        return self

    model_config = ConfigDict(from_attributes=True)


class CardResponse(CardSchema):
    id: Annotated[uuid.UUID, Field()]
