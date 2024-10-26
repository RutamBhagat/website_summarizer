from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any

from app.api.deps import get_current_user, get_db
from app import crud
from app.models.user import User
from app.models.website import WebsiteSummaryCreate, WebsiteSummaryPublic
from app.services.website_service import WebsiteService

router = APIRouter()
website_service = WebsiteService()


# Authenticated routes (commented out)
@router.post("/summarize", response_model=WebsiteSummaryPublic)
def create_summary(
    *,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    summary_in: WebsiteSummaryCreate,
) -> Any:
    """
    Create website summary for authenticated user.
    """
    # Fetch website content
    title, content = website_service.fetch_website_content(summary_in.url)
    # Generate summary
    summary = website_service.generate_summary(title, content)
    # Save to database
    db_summary = crud.create_website_summary(
        session=session,
        url=summary_in.url,
        title=title,
        summary=summary,
        owner_id=current_user.id,
    )
    return db_summary


@router.get("/summaries", response_model=list[WebsiteSummaryPublic])
def read_summaries(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve summaries for current user.
    """
    summaries = crud.get_user_summaries(
        session=session, owner_id=current_user.id, skip=skip, limit=limit
    )
    return summaries


# New routes without authentication
@router.post("/public/summarize", response_model=WebsiteSummaryPublic)
def create_public_summary(
    *,
    session: Session = Depends(get_db),
    summary_in: WebsiteSummaryCreate,
) -> Any:
    """
    Create website summary without authentication.
    """
    # Fetch website content
    title, content = website_service.fetch_website_content(summary_in.url)
    # Generate summary
    summary = website_service.generate_summary(title, content)
    # Save to database
    db_summary = crud.create_public_website_summary(
        session=session,
        url=summary_in.url,
        title=title,
        summary=summary,
    )
    return db_summary


@router.get("/public/summaries", response_model=list[WebsiteSummaryPublic])
def read_public_summaries(
    session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all public summaries.
    """
    summaries = crud.get_public_summaries(session=session, skip=skip, limit=limit)
    return summaries


@router.get("/public/summaries/{summary_id}", response_model=WebsiteSummaryPublic)
def get_public_summary_by_id(
    *, session: Session = Depends(get_db), summary_id: UUID
) -> WebsiteSummaryPublic:
    """
    Retrieve a public summary by its ID.
    """
    summary = crud.get_public_summary_by_id(session=session, summary_id=summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
