from datetime import datetime, timezone

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.core.security import DUMMY_HASH, get_password_hash, verify_password
from app.schemas.user import UserCreate, UserResponse, UserUpdate


def _doc_to_response(doc: dict) -> UserResponse:
    return UserResponse(
        id=str(doc["_id"]),
        email=doc["email"],
        full_name=doc["full_name"],
        is_active=doc["is_active"],
        created_at=doc["created_at"],
        updated_at=doc["updated_at"],
    )


class UserService:
    COLLECTION = "users"

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.db = db
        self.collection = db[self.COLLECTION]

    async def create_user(self, user_in: UserCreate) -> UserResponse:
        now = datetime.now(timezone.utc)
        document = {
            "email": user_in.email,
            "full_name": user_in.full_name,
            "hashed_password": get_password_hash(user_in.password),
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }
        try:
            result = await self.collection.insert_one(document)
        except DuplicateKeyError:
            raise ValueError("A user with this email already exists.")

        document["_id"] = result.inserted_id
        return _doc_to_response(document)

    async def authenticate_user(
        self, email: str, password: str
    ) -> UserResponse | None:
        doc = await self.collection.find_one({"email": email})
        if doc is None:
            verify_password(password, DUMMY_HASH)
            return None
        if not verify_password(password, doc["hashed_password"]):
            return None
        return _doc_to_response(doc)

    async def get_user_by_id(self, user_id: str) -> UserResponse | None:
        if not ObjectId.is_valid(user_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        if doc is None:
            return None
        return _doc_to_response(doc)

    async def get_user_by_email(self, email: str) -> UserResponse | None:
        doc = await self.collection.find_one({"email": email})
        if doc is None:
            return None
        return _doc_to_response(doc)

    async def update_user(
        self, user_id: str, user_in: UserUpdate
    ) -> UserResponse | None:
        if not ObjectId.is_valid(user_id):
            return None

        update_data = user_in.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_user_by_id(user_id)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        update_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(user_id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        if result is None:
            return None
        return _doc_to_response(result)
