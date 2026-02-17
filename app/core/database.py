import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient | None = None
    db: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        settings = get_settings()
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.DATABASE_NAME]
        await self._ensure_indexes()

    async def disconnect(self) -> None:
        if self.client:
            self.client.close()

    async def _ensure_indexes(self) -> None:
        if self.db is not None:
            try:
                await self.db.users.create_index("email", unique=True)
            except Exception as e:
                logger.warning(
                    "Could not create indexes (check DB user permissions): %s", e
                )


database = Database()


async def get_database() -> AsyncIOMotorDatabase:
    if database.db is None:
        raise RuntimeError("Database not initialized. Check lifespan events.")
    return database.db
