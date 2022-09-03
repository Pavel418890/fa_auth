from typing import Optional
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
        return await db.scalar(select(User).where(email == email))

    async def create(self, db: AsyncSession, *, data: UserCreate) -> User:
        db_obj = User(
            id=uuid4(),
            email=data.email,
            phone=data.phone,
            hashed_password=get_password_hash(data.password),
            profile=Profile(),
            is_superuser=data.is_superuser
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self, db: AsyncSession, *, email: str, password: str
    ) -> Optional[User]:
        try:
            user = await self.get_by_email(db, email=email)
            assert user
            assert verify_password(password, user.hashed_password)
        except AssertionError:
            return None
        else:
            return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
