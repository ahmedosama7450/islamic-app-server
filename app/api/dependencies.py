from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import get_settings
from app.core.database import get_database
from app.core.security import decode_access_token
from app.schemas.auth import TokenPayload
from app.schemas.user import UserResponse
from app.services.hadith_service import HadithService
from app.services.narrator_service import NarratorService
from app.services.user_service import UserService

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
)


def get_user_service(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> UserService:
    return UserService(db)


def get_hadith_service(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> HadithService:
    return HadithService(db)


def get_narrator_service(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_database)],
) -> NarratorService:
    return NarratorService(db)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, Exception):
        raise credentials_exception

    user = await user_service.get_user_by_id(token_data.sub)
    if user is None:
        raise credentials_exception
    return user
