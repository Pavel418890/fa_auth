from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core import security
from app.db.session import AsyncSessionLocal
from app import crud, schemas, models

oauth2_token = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1}/login/access-token"
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(
        *, db: AsyncSession, token: str = Depends(oauth2_token)
) -> Optional[models.User]:
    creadentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = security.verify_access_token(token)
        assert payload
        token_data = schemas.TokenPayload(**payload)
    except (AssertionError, ValidationError):
        raise creadentials_exception
    else:
        user = await crud.user.get(db, token_data.sub)
        if not user:
            raise creadentials_exception

        return user


async def get_current_active_user(
        current_user: models.User = Depends(get_current_user)
) -> models.User:
    if not await crud.user.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_active_superuser(
        current_user: models.User = Depends(get_current_active_user)
) -> models.User:
    if not await crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges"
        )
    return current_user
