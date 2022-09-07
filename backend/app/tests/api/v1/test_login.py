import pytest
from httpx import AsyncClient

from app.core.config import settings
from app.tests.utils import random_email_address, random_lower_string


async def test_get_access_token(event_loop, client: AsyncClient) -> None:
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


async def test_invalid_credentials(event_loop, client: AsyncClient) -> None:
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
