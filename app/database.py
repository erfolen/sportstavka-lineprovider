"""Настройка для базданной."""
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (create_async_engine, async_sessionmaker)

from config import data_base_url

async_engine = create_async_engine(data_base_url())
async_session_fabric = async_sessionmaker(async_engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
