from uuid import UUID
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlmodel import Session
from typing import Any

from starlette.responses import StreamingResponse
from app.api.deps import get_current_user, get_db
from app import crud
from app.models.brochure import BrochureCreate, BrochurePublic, BrochuresPublic
from app.models.user import User
from app.services.brochure_service import BrochureService

router = APIRouter()
brochure_service = BrochureService()


# New brochure endpoints
@router.post("/brochure", response_model=BrochurePublic)
async def create_brochure(
    *,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    brochure_in: BrochureCreate,
) -> Any:
    """
    Create company brochure for authenticated user.
    """
    # Generate brochure content
    content = brochure_service.generate_brochure(
        company_name=brochure_in.company_name,
        url=brochure_in.url,
    )

    # Save to database
    db_brochure = crud.create_brochure(
        session=session,
        url=brochure_in.url,
        company_name=brochure_in.company_name,
        content=content,
        owner_id=current_user.id,
    )
    return db_brochure


@router.post("/public/brochure", response_model=BrochurePublic)
async def create_public_brochure(
    *,
    session: Session = Depends(get_db),
    brochure_in: BrochureCreate,
) -> Any:
    """
    Create public company brochure without authentication.
    """
    # Generate brochure content
    content = brochure_service.generate_brochure(
        company_name=brochure_in.company_name,
        url=brochure_in.url,
    )

    # Save to database
    db_brochure = crud.create_brochure(
        session=session,
        url=brochure_in.url,
        company_name=brochure_in.company_name,
        content=content,
    )
    return db_brochure


@router.post("/brochure/stream")
async def create_streaming_brochure(
    *,
    brochure_in: BrochureCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StreamingResponse:
    """
    Create company brochure with streaming response for authenticated user.
    """

    async def generate():
        full_content = []
        async for chunk in brochure_service.stream_brochure(
            company_name=brochure_in.company_name,
            url=brochure_in.url,
        ):
            full_content.append(chunk)
            yield chunk

        # Save the complete brochure after streaming
        content = "".join(full_content)
        background_tasks.add_task(
            crud.create_brochure,
            session=session,
            url=brochure_in.url,
            company_name=brochure_in.company_name,
            content=content,
            owner_id=current_user.id,
        )

    return StreamingResponse(generate(), media_type="text/markdown")


@router.post("/public/brochure/stream")
async def create_public_streaming_brochure(
    *,
    brochure_in: BrochureCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db),
) -> StreamingResponse:
    """
    Create public company brochure with streaming response without authentication.
    """

    async def generate():
        full_content = []
        async for chunk in brochure_service.stream_brochure(
            company_name=brochure_in.company_name,
            url=brochure_in.url,
        ):
            full_content.append(chunk)
            yield chunk

        # Save the complete brochure after streaming
        content = "".join(full_content)
        background_tasks.add_task(
            crud.create_brochure,
            session=session,
            url=brochure_in.url,
            company_name=brochure_in.company_name,
            content=content,
        )

    return StreamingResponse(generate(), media_type="text/markdown")


@router.get("/brochures", response_model=BrochuresPublic)
async def list_user_brochures(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve brochures for current user.
    """
    brochures = crud.get_user_brochures(
        session=session,
        owner_id=current_user.id,
        skip=skip,
        limit=limit,
    )
    count = crud.count_brochures(session=session, owner_id=current_user.id)
    return BrochuresPublic(data=brochures, count=count)


@router.get("/public/brochures", response_model=BrochuresPublic)
async def list_public_brochures(
    session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve all public brochures.
    """
    brochures = crud.get_public_brochures(session=session, skip=skip, limit=limit)
    count = crud.count_brochures(session=session)
    return BrochuresPublic(data=brochures, count=count)


@router.get("/brochures/{brochure_id}", response_model=BrochurePublic)
async def get_brochure(
    *,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    brochure_id: UUID,
) -> Any:
    """
    Get a specific brochure by ID.
    """
    brochure = crud.get_brochure_by_id(session=session, brochure_id=brochure_id)
    if not brochure:
        raise HTTPException(status_code=404, detail="Brochure not found")
    if brochure.owner_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return brochure


@router.get("/public/brochures/{brochure_id}", response_model=BrochurePublic)
async def get_public_brochure(
    *,
    session: Session = Depends(get_db),
    brochure_id: UUID,
) -> Any:
    """
    Get a specific public brochure by ID.
    """
    brochure = crud.get_brochure_by_id(session=session, brochure_id=brochure_id)
    if not brochure or brochure.owner_id is not None:
        raise HTTPException(status_code=404, detail="Brochure not found")
    return brochure
