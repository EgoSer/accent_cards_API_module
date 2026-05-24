import uuid
from typing import Annotated

import bcrypt
from pydantic import BaseModel, ConfigDict, Field, field_validator


class AdminSchema(BaseModel):
    username: str
    password: bytes | str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("password", mode="before")
    def password_validator(cls, value):
        if isinstance(value, bytes):
            return value

        if isinstance(value, str):
            bytes_var = value.encode("utf-8")
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes_var, salt)
            return hash

        raise ValueError("Password should be a string or hashed bytes string")


class AdminResponse(AdminSchema):
    id: Annotated[uuid.UUID, Field()]
