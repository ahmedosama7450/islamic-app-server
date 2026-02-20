import re

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.schemas.hadith import HadithListResponse, HadithNarratorResponse, HadithResponse


def _doc_to_response(doc: dict) -> HadithResponse:
    return HadithResponse(
        id=str(doc["_id"]),
        book_id=doc["book_id"],
        page_number=doc["page_number"],
        full_text=doc["full_text"],
        full_text_plain=doc["full_text_plain"],
        matn=doc["matn"],
        matn_plain=doc["matn_plain"],
        narrators=[
            HadithNarratorResponse(
                id=n["id"],
                name=n["name"],
                name_plain=n["name_plain"],
            )
            for n in doc.get("narrators", [])
        ],
    )


class HadithService:
    COLLECTION = "hadiths"

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = db[self.COLLECTION]

    async def search_hadiths(
        self,
        full_text_plain: str | None = None,
        book_id: int | None = None,
        narrators: str | None = None,
        narrators_ordered: bool = False,
        skip: int = 0,
        limit: int = 20,
    ) -> HadithListResponse:
        query: dict = {}

        if full_text_plain:
            query["full_text_plain"] = {
                "$regex": re.escape(full_text_plain),
                "$options": "i",
            }

        if book_id is not None:
            query["book_id"] = book_id

        if narrators:
            narrator_ids = [int(nid.strip()) for nid in narrators.split(",") if nid.strip()]
            if narrator_ids:
                if narrators_ordered and len(narrator_ids) > 1:
                    # All narrators must exist
                    query["narrators.id"] = {"$all": narrator_ids}
                    # Each narrator must appear before the next in the array
                    order_conditions = [
                        {
                            "$lt": [
                                {"$indexOfArray": ["$narrators.id", narrator_ids[i]]},
                                {"$indexOfArray": ["$narrators.id", narrator_ids[i + 1]]},
                            ]
                        }
                        for i in range(len(narrator_ids) - 1)
                    ]
                    query["$expr"] = {"$and": order_conditions}
                else:
                    query["narrators.id"] = {"$all": narrator_ids}

        total = await self.collection.count_documents(query)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        items = [_doc_to_response(doc) async for doc in cursor]

        return HadithListResponse(items=items, total=total)

    async def get_hadith_by_id(self, hadith_id: str) -> HadithResponse | None:
        if not ObjectId.is_valid(hadith_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(hadith_id)})
        if doc is None:
            return None
        return _doc_to_response(doc)
