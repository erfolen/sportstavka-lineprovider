"""Настройка для базданной."""
from sqlalchemy import MetaData, NullPool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker,
                                    AsyncSession, AsyncEngine)

from config import data_base_url


async_engine: AsyncEngine = create_async_engine(data_base_url(), poolclass=NullPool)
async_session_fabric = async_sessionmaker(bind=async_engine,
                                          class_=AsyncSession)

# metadata = MetaData()

class Base(DeclarativeBase):
    pass

async def get_async_session() -> AsyncSession:
    async with async_session_fabric() as async_session:
        yield async_session
