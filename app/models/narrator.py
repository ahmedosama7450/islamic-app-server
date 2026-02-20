from pydantic import BaseModel, ConfigDict, Field

from app.models.user import PyObjectId


class JarhWaTadil(BaseModel):
    """Scholar evaluation entry."""

    scholar: str
    quotes: list[str] = []


class NarratorDocument(BaseModel):
    """Internal representation of a narrator document in MongoDB."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: PyObjectId = Field(alias="_id")
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
    jarh_wa_tadil: list[JarhWaTadil] = []
