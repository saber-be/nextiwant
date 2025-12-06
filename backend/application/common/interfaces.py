from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol

from backend.domain.users.entities import UserId


class PasswordHasher(Protocol):
    def hash(self, raw_password: str) -> str:
        ...

    def verify(self, raw_password: str, password_hash: str) -> bool:
        ...


@dataclass(frozen=True, slots=True)
class AuthToken:
    access_token: str
    expires_at: datetime


class TokenService(Protocol):
    def create_access_token(self, user_id: UserId, expires_delta: timedelta | None = None) -> AuthToken:
        ...


class Clock(Protocol):
    def now(self) -> datetime:
        ...
