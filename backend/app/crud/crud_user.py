from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, db: Session, *, data: UserCreate) -> User:
        db_obj = User(email=data.email)
