from uuid import UUID

from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app import crud, schemas
from app.core.config import settings
from app.tests.utils import utils
from app.tests.utils.user import create_random_user


async def test_create_user(
    client: AsyncClient,
    db: AsyncSession,
    superuser_token_headers: dict[str, str],
) -> None:
    email = utils.random_email_address()
    password = utils.random_lower_string()
    data = {"email": email, "password": password}
    response = await client.post(
        f"{settings.API_V1}/users/",
        headers=superuser_token_headers,
        json=data,
    )
    result = response.json()
    user = await crud.user.get(db, id=result["id"])
    assert response.status_code == 201
    assert user
    assert user.email == email


async def test_create_existing_user(
    client: AsyncClient,
    superuser_token_headers: dict[str, str],
) -> None:
    email = settings.INACTIVE_USER_EMAIL
    password = settings.INACTIVE_USER_PASSWORD
    data = {"email": email, "password": password}
    response = await client.post(
        f"{settings.API_V1}/users/", headers=superuser_token_headers, json=data
    )
    exc = response.json()
    assert response.status_code == 409
    assert exc["detail"] == "The user with this email already exist"


async def test_retrieve_users_by_superuser(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1}/users/", headers=superuser_token_headers
    )
    users = response.json()
    assert response.status_code == 200
    assert len(users) > 1
    for user in users:
        assert "email" in user or "phone" in user


async def test_retrieve_users_by_regular_user(
    client: AsyncClient, regular_user_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1}/users/", headers=regular_user_token_headers
    )
    exc = response.json()
    assert response.status_code == 403
    assert exc["detail"] == "The user doesn't have enough privileges"


async def test_get_me_as_superuser(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1}/users/me", headers=superuser_token_headers
    )
    result = response.json()
    assert response.status_code == 200
    assert result["email"] == settings.PRIMARY_SUPERUSER_EMAIL
    assert result["phone"] == settings.PRIMARY_SUPERUSER_PHONE
    assert result["is_active"]
    assert result["is_superuser"]


async def test_get_me_as_regular_user(
    client: AsyncClient, regular_user_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1}/users/me", headers=regular_user_token_headers
    )
    result = response.json()
    assert response.status_code == 200
    assert result["email"] == settings.TEST_USER_EMAIL
    assert result["is_active"]
    assert not result["is_superuser"]


async def test_update_me(
    client: AsyncClient, db: AsyncSession, sqla_engine: AsyncEngine
) -> None:
    current_email = utils.random_email_address()
    current_password = utils.random_lower_string()
    current_phone = utils.random_phone_string()
    conn = await sqla_engine.connect()
    async with AsyncSession(conn) as session:
        await crud.user.create(
            session,
            data=schemas.UserCreate(
                email=current_email,
                password=current_password,
                phone=current_phone,
            ),
        )
    await conn.close()

    new_email = utils.random_email_address()
    new_password = utils.random_lower_string()
    new_phone = utils.random_phone_string()
    new_user = {
        "email": new_email,
        "password": new_password,
        "phone": new_phone,
    }
    token_headers = await utils.get_token_headers(
        client=client, username=current_email, password=current_password
    )
    response = await client.put(
        f"{settings.API_V1}/users/me", headers=token_headers, json=new_user
    )
    updated_user = response.json()

    assert response.status_code == 200
    assert updated_user["email"] == new_email and updated_user["email"] != current_email
    assert updated_user["phone"] == new_phone and updated_user["phone"] != current_phone


async def test_get_user_by_id(
    client: AsyncClient,
    db: AsyncSession,
    superuser_token_headers: dict[str, str],
) -> None:
    some_user = await crud.user.get_by_email(db, email=settings.TEST_USER_EMAIL)
    response = await client.get(
        f"{settings.API_V1}/users/{some_user.id}",
        headers=superuser_token_headers,
    )
    result = response.json()
    assert response.status_code == 200
    assert result["email"] == some_user.email
    assert result["id"] == str(some_user.id)


async def test_update_user_by_id(
    client: AsyncClient,
    sqla_engine: AsyncEngine,
    superuser_token_headers: dict[str, str],
) -> None:
    email = None
    id_ = None
    conn = await sqla_engine.connect()
    async with AsyncSession(conn) as session:
        user = await create_random_user(session)
        email = user.email
        id_ = user.id
    await conn.close()

    response = await client.put(
        f"{settings.API_V1}/users/{id_}",
        headers=superuser_token_headers,
        json=schemas.UserUpdate(
            email=utils.random_email_address(),
            password=utils.random_lower_string(),
            is_active=False,
            phone=utils.random_phone_string(),
        ).dict(),
    )
    result = response.json()
    assert response.status_code == 200
    assert result["email"] != email
    assert result["id"] == str(id_)
    assert result["phone"]
    assert not result["is_active"]
    assert not result["is_superuser"]
