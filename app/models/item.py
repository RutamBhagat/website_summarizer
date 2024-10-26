# app/models/item.py
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
import uuid
from .base import BaseModel
from .user import User


class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


class Item(BaseModel, table=True):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id",
        nullable=True,
        ondelete="CASCADE",
    )
    owner: Optional[User] = Relationship(
        back_populates="items", sa_relationship_kwargs={"lazy": "selectin"}
    )


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
