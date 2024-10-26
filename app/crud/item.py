# app/crud/item.py
import uuid
from sqlmodel import Session, select
from app.models import Item, ItemCreate


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_public_item(*, session: Session, item_in: ItemCreate) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": None})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_all_items(*, session: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return session.exec(select(Item).offset(skip).limit(limit)).all()
