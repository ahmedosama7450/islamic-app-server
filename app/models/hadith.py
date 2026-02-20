from pydantic import BaseModel, ConfigDict, Field

from app.models.user import PyObjectId


class HadithNarrator(BaseModel):
    """Embedded narrator reference within a hadith document."""

    id: int
    name: str
    name_plain: str


class HadithDocument(BaseModel):
    """Internal representation of a hadith document in MongoDB."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    id: PyObjectId = Field(alias="_id")
    book_id: int
    page_number: int
    full_text: str
    full_text_plain: str
    matn: str
    matn_plain: str
    narrators: list[HadithNarrator] = []
