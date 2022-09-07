import asyncio
from typing import Generator, Iterator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.tests.utils import get_superuser_token_headers
from main import app


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="module")
async def client() -> Generator:
    async with AsyncClient(app=app, base_url="http://localhost:8000") as cli:
        yield cli


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Iterator[asyncio.events.AbstractEventLoop]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="module")
async def superuser_token_headers(client: AsyncClient) -> dict[str, str]:
    return await get_superuser_token_headers(client)
