from httpx import AsyncClient
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.core.config import settings
from app.tests.utils import utils


async def create_random_user(db: AsyncSession) -> models.User:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(email=email, password=password)
    new_user = await crud.user.create(db, data=new_user_data)
    return new_user
