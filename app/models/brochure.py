# app/models/brochure.py
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel
import uuid
from .base import TimestampModel

if TYPE_CHECKING:
    from .user import User


class BrochureBase(SQLModel):
    url: str = Field(max_length=2048, index=True)
    company_name: str = Field(max_length=255)
    content: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Brochure(TimestampModel, table=True):
    __tablename__ = "brochure"

    url: str = Field(max_length=2048, index=True)
    company_name: str = Field(max_length=255)
    content: str | None = Field(default=None)
    owner_id: uuid.UUID | None = Field(
        foreign_key="user.id", nullable=True, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(
        back_populates="brochures", sa_relationship_kwargs={"lazy": "selectin"}
    )


class BrochureCreate(SQLModel):
    url: str = Field(max_length=2048)
    company_name: str = Field(max_length=255)


class BrochurePublic(BrochureBase):
    id: uuid.UUID
    owner_id: uuid.UUID | None


class BrochuresPublic(SQLModel):
    data: list[BrochurePublic]
    count: int
