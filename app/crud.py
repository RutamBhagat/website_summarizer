import uuid
from typing import Any
from sqlmodel import Session, select
from app.core.security import get_password_hash, verify_password
from app.models import Item, ItemCreate, User, UserCreate, UserUpdate, WebsiteSummary


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_website_summary(
    *, session: Session, url: str, title: str, summary: str, owner_id: uuid.UUID
) -> WebsiteSummary:
    db_obj = WebsiteSummary(url=url, title=title, summary=summary, owner_id=owner_id)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_summaries(
    *, session: Session, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> list[WebsiteSummary]:
    return session.exec(
        select(WebsiteSummary)
        .where(WebsiteSummary.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
    ).all()


# New functions without authentication
def create_public_item(*, session: Session, item_in: ItemCreate) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": None})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_public_website_summary(
    *, session: Session, url: str, title: str, summary: str
) -> WebsiteSummary:
    db_obj = WebsiteSummary(url=url, title=title, summary=summary, owner_id=None)
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_public_summaries(
    *, session: Session, skip: int = 0, limit: int = 100
) -> list[WebsiteSummary]:
    return session.exec(
        select(WebsiteSummary)
        .where(WebsiteSummary.owner_id.is_(None))  # Select only public summaries
        .offset(skip)
        .limit(limit)
    ).all()


def get_public_summary_by_id(
    *, session: Session, summary_id: uuid.UUID
) -> WebsiteSummary | None:
    return session.exec(
        select(WebsiteSummary)
        .where(WebsiteSummary.id == summary_id)
        .where(WebsiteSummary.owner_id.is_(None))  # Ensure it's a public summary
    ).first()


def get_all_items(*, session: Session, skip: int = 0, limit: int = 100) -> list[Item]:
    return session.exec(select(Item).offset(skip).limit(limit)).all()
