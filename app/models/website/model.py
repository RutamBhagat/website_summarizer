# app/models/website/model.py
from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
import uuid
from ..base import TimestampModel

if TYPE_CHECKING:
    from ..user.model import User


class WebsiteSummary(TimestampModel, table=True):
    url: str = Field(max_length=2048, index=True)
    title: str = Field(max_length=255)
    summary: str | None = Field(default=None)
    owner_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    owner: Optional["User"] = Relationship(
        back_populates="website_summaries",  # Match the new name in User model
        sa_relationship_kwargs={"lazy": "selectin"},
    )
