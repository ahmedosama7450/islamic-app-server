from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_hadith_service
from app.schemas.hadith import HadithListResponse, HadithResponse
from app.services.hadith_service import HadithService

router = APIRouter(prefix="/hadiths", tags=["hadiths"])


@router.get("", response_model=HadithListResponse)
async def search_hadiths(
    hadith_service: Annotated[HadithService, Depends(get_hadith_service)],
    full_text_plain: Annotated[str | None, Query()] = None,
    book_id: Annotated[int | None, Query()] = None,
    narrators: Annotated[str | None, Query(description="Comma-separated narrator IDs")] = None,
    narrators_ordered: Annotated[bool, Query(description="If true, narrators must appear in the given order")] = False,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> HadithListResponse:
    return await hadith_service.search_hadiths(
        full_text_plain=full_text_plain,
        book_id=book_id,
        narrators=narrators,
        narrators_ordered=narrators_ordered,
        skip=skip,
        limit=limit,
    )


@router.get("/{hadith_id}", response_model=HadithResponse)
async def get_hadith(
    hadith_id: str,
    hadith_service: Annotated[HadithService, Depends(get_hadith_service)],
) -> HadithResponse:
    hadith = await hadith_service.get_hadith_by_id(hadith_id)
    if hadith is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hadith not found.",
        )
    return hadith
