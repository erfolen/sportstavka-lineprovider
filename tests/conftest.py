"""Настройки тестового окружения."""
import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)

from config import data_test_base_url
from app.migrations.env import target_metadata
from app.main import app
from app.database import async_session_fabric

# DATABASE
async_test_engine = create_async_engine(data_test_base_url(), future=True,
                                        echo=True)
async_test_session_fabric = async_sessionmaker(async_test_engine,
                                               class_=AsyncSession,
                                               expire_on_commit=False)

target_metadata.bind = async_test_engine


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session_fabric() as session:
        yield session


app.dependency_overrides[async_session_fabric] = override_get_async_session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Управлять сессиями в тестах."""
    async with async_test_session_fabric() as session:
        yield session

@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with async_test_engine.begin() as conn:
        await conn.run_sync(target_metadata.create_all)
    yield
    async with async_test_engine.begin() as conn:
        await conn.run_sync(target_metadata.drop_all)

# SETUP
@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
