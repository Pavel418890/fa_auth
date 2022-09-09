from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

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
    db: AsyncSession,
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
