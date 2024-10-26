# app/models/base.py
from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


class TimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
