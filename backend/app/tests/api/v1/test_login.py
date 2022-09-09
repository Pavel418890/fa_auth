from httpx import AsyncClient

from app import crud, schemas
from app.core.config import settings
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email_address, random_lower_string


async def test_get_access_token(client: AsyncClient) -> None:
    login_data = {
        "username": settings.PRIMARY_SUPERUSER_EMAIL,
        "password": settings.PRIMARY_SUPERUSER_PASSWORD,
    }
    r = await client.post(
        f"{settings.API_V1}/login/access-token", data=login_data
    )
    token = r.json()
    assert r.status_code == 200
    assert token["token_type"] == "bearer"
    assert token["access_token"]


async def test_create_access_token_invalid_credentials(
    client: AsyncClient,
) -> None:
    login_data = {
        "username": random_email_address(),
        "password": random_lower_string(),
    }
    response = await client.post(
        f"{settings.API_V1}/login/access-token", data=login_data
    )
    exc = response.json()
    assert response.status_code == 401
    assert exc["detail"] == "Incorrect email or password"


async def test_create_access_token_inactive_user(client: AsyncClient) -> None:
    login_data = {
        "username": settings.INACTIVE_USER_EMAIL,
        "password": settings.INACTIVE_USER_PASSWORD,
    }
    response = await client.post(
        f"{settings.API_V1}/login/access-token", data=login_data
    )
    exc = response.json()
    assert response.status_code == 401
    assert exc["detail"] == "Inactive user"


async def test_use_access_token(
    client: AsyncClient, superuser_token_headers: dict[str, str]
) -> None:
    response = await client.get(
        f"{settings.API_V1}/login/test-token", headers=superuser_token_headers
    )
    result = response.json()
    assert response.status_code == 200
    assert "email" in result
    assert "phone" in result
