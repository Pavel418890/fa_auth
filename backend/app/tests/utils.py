import asyncio
import random
import string

from httpx import AsyncClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email_address() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_phone_string() -> str:
    return f'+{"".join(random.choices(string.digits, k=11))}'


async def get_superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    login_data = {
        "username": settings.PRIMARY_SUPERUSER_EMAIL,
        "password": settings.PRIMARY_SUPERUSER_PASSWORD,
    }
    r = await client.post(
        f"{settings.API_V1}/login/access-token", data=login_data
    )
    token = r.json()
    access_token = token["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
