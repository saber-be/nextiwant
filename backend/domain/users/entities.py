from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class UserId:
    value: UUID

    @staticmethod
    def new() -> "UserId":
        return UserId(value=uuid4())


@dataclass(slots=True)
class User:
    id: UserId
    email: str
    password_hash: str
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def activate(self) -> None:
        if not self.is_active:
            self.is_active = True
            self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        if self.is_active:
            self.is_active = False
            self.updated_at = datetime.utcnow()

    def change_password_hash(self, new_hash: str) -> None:
        if not new_hash:
            raise ValueError("Password hash cannot be empty")
        if new_hash == self.password_hash:
            return
        self.password_hash = new_hash
        self.updated_at = datetime.utcnow()


@dataclass(slots=True)
class UserProfile:
    user_id: UserId
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    photo_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def name(self) -> str:
        parts = [p for p in [self.first_name, self.last_name] if p]
        if parts:
            return " ".join(parts)
        return self.username or ""

    def update_profile(
        self,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        birthday: Optional[date] = None,
        photo_url: Optional[str] = None,
    ) -> None:
        changed = False

        if username is not None and username != self.username:
            self.username = username or None
            changed = True

        if first_name is not None and first_name != self.first_name:
            self.first_name = first_name or None
            changed = True

        if last_name is not None and last_name != self.last_name:
            self.last_name = last_name or None
            changed = True

        if birthday is not None and birthday != self.birthday:
            self.birthday = birthday
            changed = True

        if photo_url is not None and photo_url != self.photo_url:
            self.photo_url = photo_url
            changed = True

        if changed:
            self.updated_at = datetime.utcnow()
