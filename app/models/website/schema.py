# app/models/website/schema.py
from datetime import datetime
from sqlmodel import Field, SQLModel
import uuid


class WebsiteSummaryBase(SQLModel):
    url: str = Field(max_length=2048, index=True)
    title: str = Field(max_length=255)
    summary: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WebsiteSummaryPublic(WebsiteSummaryBase):
    id: uuid.UUID
    owner_id: uuid.UUID | None


class WebsiteSummaryCreate(SQLModel):
    url: str = Field(max_length=2048)
