from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401


async def init_db(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db, email=settings.PRIMARY_SUPERUSER_EMAIL)
    if not user:
        superuser = schemas.UserCreate(
            email=settings.PRIMARY_SUPERUSER_EMAIL,
            phone=settings.PRIMARY_SUPERUSER_PHONE,
            password=settings.PRIMARY_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(db, data=superuser)

    inactive_user = await crud.user.get_by_email(db, email=settings.INACTIVE_USER_EMAIL)
    if not inactive_user:
        inactive_user_data = schemas.UserCreate(
            email=settings.INACTIVE_USER_EMAIL,
            password=settings.INACTIVE_USER_PASSWORD,
        )
        new_user = await crud.user.create(db, data=inactive_user_data)
        inactive_user = await crud.user.update(
            db, user_in_db=new_user, data={"is_active": False}
        )

    test_user = await crud.user.get_by_email(db, email=settings.TEST_USER_EMAIL)
    if not test_user:
        test_user_data = schemas.UserCreate(
            email=settings.TEST_USER_EMAIL,
            password=settings.TEST_USER_PASSWORD,
        )
        await crud.user.create(db, data=test_user_data)
