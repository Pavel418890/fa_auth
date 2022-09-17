from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.core import security
from app.tests.utils import utils
from app.tests.utils.user import create_random_user


async def test_create_user(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(email=email, password=password)
    new_user = await crud.user.create(db, data=new_user_data)
    assert new_user.email == email
    assert hasattr(new_user, "hashed_password")
    assert new_user.hashed_password != password


async def test_create_user_without_email(db: AsyncSession) -> None:
    phone = utils.random_phone_string()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(phone=phone, password=password)
    new_user = await crud.user.create(db, data=new_user_data)
    assert new_user.email is None
    assert new_user.phone == phone
    assert hasattr(new_user, "hashed_password")
    assert new_user.hashed_password != password


async def test_authenticate_user(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(email=email, password=password, is_active=True)
    user = await crud.user.create(db, data=new_user_data)
    authenticated_user = await crud.user.authenticate(
        db, email=email, password=password
    )
    assert authenticated_user
    assert authenticated_user.email == user.email


async def test_not_authenticate_user(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    authenticated_user = await crud.user.authenticate(
        db, email=email, password=password
    )
    assert authenticated_user is None


async def test_check_if_user_is_active(db: AsyncSession) -> None:
    new_user = await create_random_user(db)
    assert crud.user.is_active(new_user)


async def test_check_if_user_is_active_inactive(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(email=email, password=password, is_active=False)
    new_user = await crud.user.create(db, data=new_user_data)
    assert crud.user.is_active(new_user)


async def test_check_if_user_is_superuser(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(
        email=email, password=password, is_superuser=True
    )
    new_superuser = await crud.user.create(db, data=new_user_data)
    assert crud.user.is_superuser(new_superuser)


async def test_check_if_regular_user_not_superuser(db: AsyncSession) -> None:
    new_user = await create_random_user(db)
    assert not crud.user.is_superuser(new_user)


async def test_get_user(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(email=email, password=password)
    new_user = await crud.user.create(db, data=new_user_data)
    user_in_db = await crud.user.get(db, id=new_user.id)
    assert user_in_db
    assert jsonable_encoder(user_in_db) == jsonable_encoder(new_user)


async def test_update_user(db: AsyncSession) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    new_password = utils.random_lower_string()
    new_user_data = schemas.UserCreate(
        email=email, password=password, is_superuser=True
    )
    updated_user_data = schemas.UserUpdate(password=new_password, is_superuser=True)
    new_user = await crud.user.create(db, data=new_user_data)
    await crud.user.update(db, user_in_db=new_user, data=updated_user_data)
    updated_user = await crud.user.get(db, id=new_user.id)
    assert updated_user
    assert updated_user.email == new_user.email
    assert security.verify_password(new_password, updated_user.hashed_password)
