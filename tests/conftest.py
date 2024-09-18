"""Настройки тестового окружения."""
import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)

from config import data_test_base_url
from app.model import EventBD  # noqa
from app.main import app
from app.database import async_session_fabric, Base

# DATABASE
async_test_engine = create_async_engine(data_test_base_url(), future=True,
                                        echo=True)
async_test_session_fabric = async_sessionmaker(async_test_engine,
                                               class_=AsyncSession,
                                               expire_on_commit=False)

Base.metadata.bind = async_test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session_fabric() as session:
        yield session


app.dependency_overrides[async_session_fabric] = override_get_async_session


@pytest.fixture(scope="function")
def engine():
    get_engine = async_test_engine
    yield get_engine
    get_engine.sync_engine.dispose()


@pytest.fixture(autouse=True, scope='session')
async def db_session():
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield async_test_session_fabric()
    # async with async_test_engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all(bind=async_test_engine))


# SETUP
@pytest.fixture(scope='function')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# client = TestClient(app)

# @pytest.fixture(scope="function")
# async def ac() -> AsyncGenerator[AsyncClient, None]:
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         yield ac

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as get_client:
        yield get_client


@pytest.fixture(scope="function")
async def session(engine):
    async with AsyncSession(engine) as get_session:
        yield get_session
