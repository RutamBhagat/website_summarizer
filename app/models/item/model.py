# app/models/item/model.py
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
import uuid
from ..base import BaseModel

if TYPE_CHECKING:
    from ..user.model import User


class Item(BaseModel, table=True):
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id",
        nullable=True,
        ondelete="CASCADE",
    )
    owner: Optional["User"] = Relationship(
        back_populates="items", sa_relationship_kwargs={"lazy": "selectin"}
    )
