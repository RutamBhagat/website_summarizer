# app/crud/website.py
import uuid
from sqlmodel import Session, select
from app.models import WebsiteSummary


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
        .where(WebsiteSummary.owner_id.is_(None))
        .offset(skip)
        .limit(limit)
    ).all()


def get_public_summary_by_id(
    *, session: Session, summary_id: uuid.UUID
) -> WebsiteSummary | None:
    return session.exec(
        select(WebsiteSummary)
        .where(WebsiteSummary.id == summary_id)
        .where(WebsiteSummary.owner_id.is_(None))
    ).first()
