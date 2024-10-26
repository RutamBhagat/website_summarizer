# app/models/website.py
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, Relationship, SQLModel
import uuid
from .base import TimestampModel
from .user import User


class WebsiteSummaryBase(SQLModel):
    url: str = Field(max_length=2048, index=True)
    title: str = Field(max_length=255)
    summary: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WebsiteSummary(TimestampModel, table=True):
    url: str = Field(max_length=2048, index=True)
    title: str = Field(max_length=255)
    summary: str | None = Field(default=None)
    owner_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    owner: Optional[User] = Relationship(
        back_populates="website_summaries", sa_relationship_kwargs={"lazy": "selectin"}
    )


class WebsiteSummaryCreate(SQLModel):
    url: str = Field(max_length=2048)


class WebsiteSummaryPublic(WebsiteSummaryBase):
    id: uuid.UUID
    owner_id: uuid.UUID | None


# New Brochure Models
class BrochureBase(SQLModel):
    url: str = Field(max_length=2048, index=True)
    company_name: str = Field(max_length=255)
    content: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Brochure(TimestampModel, table=True):
    url: str = Field(max_length=2048, index=True)
    company_name: str = Field(max_length=255)
    content: str = Field(default=None)
    owner_id: uuid.UUID | None = Field(foreign_key="user.id", nullable=True)
    owner: Optional[User] = Relationship(
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
