from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Any

from app.api.deps import get_current_user, get_db
from app.services.website_service import WebsiteService
from app.models import WebsiteSummaryCreate, WebsiteSummaryPublic, User
from app import crud

router = APIRouter()
website_service = WebsiteService()


@router.post("/summarize", response_model=WebsiteSummaryPublic)
def create_summary(
    *,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    summary_in: WebsiteSummaryCreate
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
