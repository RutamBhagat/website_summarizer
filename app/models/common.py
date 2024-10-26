# app/models/common.py
from sqlmodel import SQLModel


class Message(SQLModel):
    message: str
