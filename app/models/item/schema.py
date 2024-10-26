# app/models/item/schema.py
from sqlmodel import Field, SQLModel
import uuid


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)


class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID | None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int
