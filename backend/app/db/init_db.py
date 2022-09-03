from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401
from app.core.config import settings


async def init_db(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(
        db, email=settings.PRIMARY_SUPERUSER_EMAIL
    )
    if not user:
        superuser = schemas.UserCreate(
            email=settings.PRIMARY_SUPERUSER_EMAIL,
            phone=settings.PRIMARY_SUPERUSER_PHONE,
            password=settings.PRIMARY_SUPERUSER_PASSWORD,
            full_name=settings.PRIMARY_SUPERUSER_NAME,
            is_superuser=True,
        )
        await crud.user.create(db, data=superuser)
