from pydantic import BaseModel


class HadithNarratorResponse(BaseModel):
    id: int
    name: str
    name_plain: str


class HadithResponse(BaseModel):
    id: str
    book_id: int
    page_number: int
    full_text: str
    full_text_plain: str
    matn: str
    matn_plain: str
    narrators: list[HadithNarratorResponse] = []


class HadithListResponse(BaseModel):
    items: list[HadithResponse]
    total: int
