from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional, Protocol

from .entities import User, UserId, UserProfile


class UserRepository(Protocol):
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        ...

    async def get_by_email(self, email: str) -> Optional[User]:
        ...

    async def add(self, user: User) -> None:
        ...

    async def update(self, user: User) -> None:
        ...


class UserProfileRepository(Protocol):
    async def get_by_user_id(self, user_id: UserId) -> Optional[UserProfile]:
        ...

    async def add(self, profile: UserProfile) -> None:
        ...

    async def update(self, profile: UserProfile) -> None:
        ...


class UnitOfWork(ABC):
    users: UserRepository
    profiles: UserProfileRepository

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        ...

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:
        ...

    @abstractmethod
    async def commit(self) -> None:
        ...

    @abstractmethod
    async def rollback(self) -> None:
        ...
