# app/models/__init__.py
from .base import BaseModel, TimestampModel
from .common import Message
from .user import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    UserUpdateMe,
    UserPublic,
    UsersPublic,
    UserRegister,
)
from .item import Item, ItemBase, ItemCreate, ItemUpdate, ItemPublic, ItemsPublic
from .website import (
    WebsiteSummary,
    WebsiteSummaryBase,
    WebsiteSummaryCreate,
    WebsiteSummaryPublic,
)
from .auth import Token, TokenPayload, UpdatePassword, NewPassword
from .brochure import (  # Add this new import
    Brochure,
    BrochureBase,
    BrochureCreate,
    BrochurePublic,
    BrochuresPublic,
)

__all__ = [
    # Base models
    "BaseModel",
    "TimestampModel",
    # Common models
    "Message",
    # User models
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserUpdateMe",
    "UserPublic",
    "UsersPublic",
    "UserRegister",
    # Item models
    "Item",
    "ItemBase",
    "ItemCreate",
    "ItemUpdate",
    "ItemPublic",
    "ItemsPublic",
    # Website models
    "WebsiteSummary",
    "WebsiteSummaryBase",
    "WebsiteSummaryCreate",
    "WebsiteSummaryPublic",
    # Auth models
    "Token",
    "TokenPayload",
    "UpdatePassword",
    "NewPassword",
    # Brochure models
    "Brochure",
    "BrochureBase",
    "BrochureCreate",
    "BrochurePublic",
    "BrochuresPublic",
]
