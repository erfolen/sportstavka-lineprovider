"""Настройки тестового окружения."""
from typing import AsyncGenerator

import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from  sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession)

from config import data_test_base_url, sync_test_base_url
from app.model import EventBD  # noqa
from app.main import app
from app.database import Base, get_async_session#, metadata
from sqlalchemy.pool import NullPool

# DATABASE
async_test_engine = create_async_engine(data_test_base_url(),
                                        poolclass=NullPool)
async_test_session_fabric = async_sessionmaker(async_test_engine,
                                               class_=AsyncSession,
                                               expire_on_commit=False)
Base.metadata.bind = async_test_engine

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session_fabric() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(scope="session")
def engine() -> None:
    yield async_test_engine
    async_test_engine.sync_engine.dispose()

@pytest.fixture(autouse=True, scope='session')
def prepare_database() -> None:
    """Create Tables via our metadata in TEST DB and drop them after tests."""
    sync_engine_test = create_engine(sync_test_base_url(), echo=True)
    Base.metadata.create_all(sync_engine_test)
    yield
    Base.metadata.drop_all(sync_engine_test)

# SETUP
@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as get_client:
        yield get_client


@pytest.fixture(scope="session")
async def session(engine):
    async with AsyncSession(engine) as get_session:
        yield get_session
