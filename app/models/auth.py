# app/models/auth.py
from pydantic import Field
from sqlmodel import SQLModel
import uuid


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: uuid.UUID | None = None


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)
