"""Настройка для базданной."""
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker, AsyncSession)

from config import data_base_url

async_engine = create_async_engine(data_base_url())
async_session_fabric = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_fabric() as session:
        yield session