from __future__ import annotations

from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_engine_and_session_factory(database_url: str) -> tuple[async_sessionmaker[AsyncSession], Base]:
    engine = create_async_engine(database_url, echo=False, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return session_factory, Base


async def get_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session
