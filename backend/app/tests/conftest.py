import asyncio
from typing import Generator, Iterator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.session import AsyncSessionLocal, async_engine
from app.main import app
from app.tests.utils import get_superuser_token_headers


@pytest_asyncio.fixture(scope="session")
async def sqla_engine() -> AsyncEngine:
    try:
        yield async_engine
    finally:
        await async_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db(sqla_engine) -> AsyncSession:
    connection = await sqla_engine.connect()
    transaction = await connection.begin()
    ASession = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession
    )
    session = ASession()
    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()


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
