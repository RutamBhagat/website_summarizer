# app/models/user/model.py
from typing import TYPE_CHECKING, List
from sqlmodel import Field, Relationship, SQLModel
from pydantic import EmailStr
import uuid
from ..base import BaseModel

if TYPE_CHECKING:
    from ..item.model import Item
    from ..website.model import WebsiteSummary


class User(BaseModel, table=True):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

    # Each relationship needs its own unique back_populates
    items: List["Item"] = Relationship(
        back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"}
    )
    website_summaries: List["WebsiteSummary"] = Relationship(  # Renamed from summaries
        back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"}
    )
