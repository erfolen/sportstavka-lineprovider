"""Fixtures for DAL functions test."""
# STDLIB
import asyncio
import os

# THIRDPARTY
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.pool import NullPool

# FIRSTPARTY
from app.model import Base
from app.model import EventBD  # NOQA
from config import


engine_test = create_async_engine(test_db_async_url, poolclass=NullPool)
async_session = async_sessionmaker(
        engine_test, expire_on_commit=False, class_=AsyncSession
    )


@pytest.fixture(scope='session')
def engine() -> None:
    """Make Async Engine for test."""
    yield engine_test
    engine_test.sync_engine.dispose()


@pytest.fixture(scope='session')
def prepare_database() -> None:
    """Create Tables via our metadata in TEST DB and drop them after tests."""
    sync_engine_test = create_engine(test_db_sync_url, echo=True)
    BaseModel.metadata.create_all(bind=sync_engine_test)
    yield
    BaseModel.metadata.drop_all(bind=sync_engine_test)


@pytest.fixture(scope='session')
def event_loop() -> None:
    """Make Event Loop for tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()