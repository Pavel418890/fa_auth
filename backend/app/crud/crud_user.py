from typing import Any, Optional, Union
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models import Profile, User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_email(
        self, db: AsyncSession, *, email: str
    ) -> Optional[User]:
        return await db.scalar(select(User).where(User.email == email))

    async def create(self, db: AsyncSession, *, data: UserCreate) -> User:
        db_obj = User(
            id=uuid4(),
            email=data.email,
            phone=data.phone,
            hashed_password=get_password_hash(data.password),
            profile=Profile(),
            is_superuser=data.is_superuser,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        try:
            user_in_db = await self.get_by_email(db, email=email)
            assert user_in_db
            assert verify_password(password, user_in_db.hashed_password)
        except AssertionError:
            return None
        else:
            return user_in_db

    async def update(
        self,
        db: AsyncSession,
        *,
        user_in_db: User,
        data: Union[UserUpdate, dict[str, Any]]
    ) -> Optional[User]:
        if isinstance(data, dict):
            update_data = data
        else:
            update_data = data.dict(exclude_unset=True)
            if update_data.get("password", None):
                hashed_password = get_password_hash(
                    update_data.pop("password")
                )
                update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=user_in_db, data=update_data)

    def is_active(self, user_in_db: User) -> bool:
        return user_in_db.is_active

    def is_superuser(self, user_in_db: User) -> bool:
        return user_in_db.is_superuser


user = CRUDUser(User)
