from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID


import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_access_token(subject: UUID | str | Any, expires_delta: timedelta) -> str:
    """
    Create a JWT access token.

    Args:
        subject: The subject identifier (typically user ID)
        expires_delta: How long the token should be valid for

    Returns:
        str: The encoded JWT token
    """
    expire = datetime.now(timezone.utc) + expires_delta

    # Convert UUID to string if necessary
    if isinstance(subject, UUID):
        subject = str(subject)
    elif not isinstance(subject, str):
        subject = str(subject)  # Convert any other type to string

    to_encode = {"exp": expire, "sub": subject}

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
