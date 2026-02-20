from pydantic import BaseModel


class JarhWaTadilResponse(BaseModel):
    scholar: str
    quotes: list[str] = []


class NarratorResponse(BaseModel):
    id: str
    narrator_id: int
    name: str
    name_plain: str
    kunya: str = ""
    nasab: str = ""
    death_date: str = ""
    tabaqa: str = ""
    rank_ibn_hajar: str = ""
    rank_dhahabi: str = ""
    relations: str = ""
    jarh_wa_tadil: list[JarhWaTadilResponse] = []


class NarratorListResponse(BaseModel):
    items: list[NarratorResponse]
    total: int
