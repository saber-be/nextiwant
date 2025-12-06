from __future__ import annotations

import os
from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.application.common.interfaces import TokenService
from backend.infrastructure.repositories.users import SqlAlchemyUsersUnitOfWork
from backend.infrastructure.repositories.wishlists import SqlAlchemyWishlistsUnitOfWork
from backend.infrastructure.services.security import JwtTokenService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://iliketohave:iliketohave_password@db:5432/iliketohave",
)

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


async def get_users_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[SqlAlchemyUsersUnitOfWork]:
    yield SqlAlchemyUsersUnitOfWork(session=session)


async def get_wishlists_uow(
    session: AsyncSession = Depends(get_session),
) -> AsyncIterator[SqlAlchemyWishlistsUnitOfWork]:
    yield SqlAlchemyWishlistsUnitOfWork(session=session)


_jwt_secret = os.getenv("JWT_SECRET", "change_me_in_production")
_jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
_access_token_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", "60"))

_token_service: TokenService = JwtTokenService(
    secret_key=_jwt_secret,
    algorithm=_jwt_algorithm,
    access_token_expires_minutes=_access_token_minutes,
)


def get_token_service() -> TokenService:
    return _token_service
