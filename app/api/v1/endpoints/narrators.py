from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_narrator_service
from app.schemas.narrator import NarratorListResponse, NarratorResponse
from app.services.narrator_service import NarratorService

router = APIRouter(prefix="/narrators", tags=["narrators"])


@router.get("", response_model=NarratorListResponse)
async def search_narrators(
    narrator_service: Annotated[NarratorService, Depends(get_narrator_service)],
    name_plain: Annotated[str | None, Query()] = None,
    kunya: Annotated[str | None, Query()] = None,
    nasab: Annotated[str | None, Query()] = None,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> NarratorListResponse:
    return await narrator_service.search_narrators(
        name_plain=name_plain,
        kunya=kunya,
        nasab=nasab,
        skip=skip,
        limit=limit,
    )


@router.get("/{narrator_id}", response_model=NarratorResponse)
async def get_narrator(
    narrator_id: str,
    narrator_service: Annotated[NarratorService, Depends(get_narrator_service)],
) -> NarratorResponse:
    narrator = await narrator_service.get_narrator_by_id(narrator_id)
    if narrator is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narrator not found.",
        )
    return narrator
