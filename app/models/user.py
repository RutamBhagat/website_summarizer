# app/models/user.py
from typing import List, Optional, TYPE_CHECKING
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
import uuid
from .base import BaseModel

if TYPE_CHECKING:
    from .item import Item
    from .website import WebsiteSummary
    from .brochure import Brochure


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class User(BaseModel, table=True):
    __tablename__ = "user"

    email: EmailStr = Field(unique=True, index=True, max_length=255)
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)

    items: List["Item"] = Relationship(
        back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"}
    )
    website_summaries: List["WebsiteSummary"] = Relationship(
        back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"}
    )
    brochures: List["Brochure"] = Relationship(
        back_populates="owner", sa_relationship_kwargs={"lazy": "selectin"}
    )


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
