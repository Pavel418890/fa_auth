from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        yield db


async def get_current_user(*, db: AsyncSession, token: OAuth2PasswordBearer =  Depends() ):
    pass


async def get_active_user():
    pass


async def get_current_superuser():
    pass
