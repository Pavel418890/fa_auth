from typing import Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
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
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
