# app/models/base.py
from datetime import datetime
import uuid
from sqlmodel import Field, SQLModel


# Base class for all models with ID
class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Base class for timestamped models
class TimestampModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
