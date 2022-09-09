import asyncio
import random
import string

from httpx import AsyncClient
from pydantic.networks import EmailStr

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email_address() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_phone_string() -> str:
    return f'+{"".join(random.choices(string.digits, k=11))}'


async def get_token_headers(
    *, client: AsyncClient, username: EmailStr, password: str
) -> dict[str, str]:
    login_data = {"username": username, "password": password}
    response = await client.post(
        f"{settings.API_V1}/login/access-token", data=login_data
    )
    token = response.json()
    access_token = token["access_token"]
    return {"Authorization": f"Bearer {access_token}"}
