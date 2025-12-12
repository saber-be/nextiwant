from __future__ import annotations

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.users.entities import User, UserId, UserProfile
from backend.domain.users.repositories import UnitOfWork as UsersUnitOfWork, UserProfileRepository, UserRepository
from backend.infrastructure.db.models import UserModel, UserProfileModel


def _user_from_model(model: UserModel) -> User:
    return User(
        id=UserId(value=model.id),
        email=model.email,
        password_hash=model.password_hash,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _user_to_model(user: User, model: Optional[UserModel] = None) -> UserModel:
    if model is None:
        model = UserModel(id=user.id.value)
    model.email = user.email
    model.password_hash = user.password_hash
    model.is_active = user.is_active
    model.created_at = user.created_at
    model.updated_at = user.updated_at
    return model


def _profile_from_model(model: UserProfileModel) -> UserProfile:
    return UserProfile(
        user_id=UserId(value=model.user_id),
        username=model.username,
        first_name=model.first_name,
        last_name=model.last_name,
        birthday=model.birthday,
        photo_url=model.photo_url,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def _profile_to_model(profile: UserProfile, model: Optional[UserProfileModel] = None) -> UserProfileModel:
    if model is None:
        model = UserProfileModel(user_id=profile.user_id.value)
    model.username = profile.username
    model.first_name = profile.first_name
    model.last_name = profile.last_name
    model.birthday = profile.birthday
    model.photo_url = profile.photo_url
    model.created_at = profile.created_at
    model.updated_at = profile.updated_at
    return model


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _user_from_model(model) if model else None

    async def add(self, user: User) -> None:
        model = _user_to_model(user)
        self._session.add(model)

    async def update(self, user: User) -> None:
        stmt = select(UserModel).where(UserModel.id == user.id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            model = UserModel(id=user.id.value)
            self._session.add(model)
        _user_to_model(user, model)


class SqlAlchemyUserProfileRepository(UserProfileRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_user_id(self, user_id: UserId) -> Optional[UserProfile]:
        stmt = select(UserProfileModel).where(UserProfileModel.user_id == user_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return _profile_from_model(model) if model else None

    async def add(self, profile: UserProfile) -> None:
        model = _profile_to_model(profile)
        self._session.add(model)

    async def update(self, profile: UserProfile) -> None:
        stmt = select(UserProfileModel).where(UserProfileModel.user_id == profile.user_id.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            model = UserProfileModel(user_id=profile.user_id.value)
            self._session.add(model)
        _profile_to_model(profile, model)


class SqlAlchemyUsersUnitOfWork(UsersUnitOfWork):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.users = SqlAlchemyUserRepository(session)
        self.profiles = SqlAlchemyUserProfileRepository(session)

    async def __aenter__(self) -> "SqlAlchemyUsersUnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if exc is not None:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
