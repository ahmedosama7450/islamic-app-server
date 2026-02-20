import re

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.narrator import (
    JarhWaTadilResponse,
    NarratorListResponse,
    NarratorResponse,
)


def _doc_to_response(doc: dict) -> NarratorResponse:
    return NarratorResponse(
        id=str(doc["_id"]),
        narrator_id=doc["narrator_id"],
        name=doc["name"],
        name_plain=doc["name_plain"],
        kunya=doc.get("kunya", ""),
        nasab=doc.get("nasab", ""),
        death_date=doc.get("death_date", ""),
        tabaqa=doc.get("tabaqa", ""),
        rank_ibn_hajar=doc.get("rank_ibn_hajar", ""),
        rank_dhahabi=doc.get("rank_dhahabi", ""),
        relations=doc.get("relations", ""),
        jarh_wa_tadil=[
            JarhWaTadilResponse(
                scholar=j["scholar"],
                quotes=j.get("quotes", []),
            )
            for j in doc.get("jarh_wa_tadil", [])
        ],
    )


class NarratorService:
    COLLECTION = "narrators"

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = db[self.COLLECTION]

    async def search_narrators(
        self,
        name_plain: str | None = None,
        kunya: str | None = None,
        nasab: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> NarratorListResponse:
        query: dict = {}

        if name_plain:
            query["name_plain"] = {"$regex": re.escape(name_plain), "$options": "i"}

        if kunya:
            query["kunya"] = {"$regex": re.escape(kunya), "$options": "i"}

        if nasab:
            query["nasab"] = {"$regex": re.escape(nasab), "$options": "i"}

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = [_doc_to_response(doc) async for doc in cursor]

        return NarratorListResponse(items=items, total=total)

    async def get_narrator_by_id(self, narrator_id: str) -> NarratorResponse | None:
        if not ObjectId.is_valid(narrator_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(narrator_id)})
        if doc is None:
            return None
        return _doc_to_response(doc)
