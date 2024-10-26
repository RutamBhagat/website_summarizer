# app/crud/brochure.py
import uuid
from typing import Optional, List
from sqlmodel import Session, select

from app.models.brochure import Brochure


# New Brochure CRUD operations
def create_brochure(
    *,
    session: Session,
    url: str,
    company_name: str,
    content: str,
    owner_id: Optional[uuid.UUID] = None,
) -> Brochure:
    db_obj = Brochure(
        url=url,
        company_name=company_name,
        content=content,
        owner_id=owner_id,
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_brochure_by_id(
    *, session: Session, brochure_id: uuid.UUID
) -> Optional[Brochure]:
    return session.exec(select(Brochure).where(Brochure.id == brochure_id)).first()


def get_user_brochures(
    *, session: Session, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
) -> List[Brochure]:
    return session.exec(
        select(Brochure).where(Brochure.owner_id == owner_id).offset(skip).limit(limit)
    ).all()


def get_public_brochures(
    *, session: Session, skip: int = 0, limit: int = 100
) -> List[Brochure]:
    return session.exec(
        select(Brochure).where(Brochure.owner_id.is_(None)).offset(skip).limit(limit)
    ).all()


def count_brochures(*, session: Session, owner_id: Optional[uuid.UUID] = None) -> int:
    query = select(Brochure)
    if owner_id is not None:
        query = query.where(Brochure.owner_id == owner_id)
    else:
        query = query.where(Brochure.owner_id.is_(None))
    return session.exec(query).count()
