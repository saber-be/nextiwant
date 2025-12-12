from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from backend.domain.users.entities import UserId, UserProfile
from backend.domain.users.repositories import UnitOfWork as UsersUnitOfWork


@dataclass(slots=True)
class GetProfileQuery:
    user_id: UserId


@dataclass(slots=True)
class GetProfileResult:
    profile: Optional[UserProfile]


class GetProfileUseCase:
    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, query: GetProfileQuery) -> GetProfileResult:
        async with self._uow as uow:
            profile = await uow.profiles.get_by_user_id(query.user_id)
        return GetProfileResult(profile=profile)


@dataclass(slots=True)
class UpsertProfileCommand:
    user_id: UserId
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birthday: Optional[date] = None
    photo_url: Optional[str] = None


@dataclass(slots=True)
class UpsertProfileResult:
    profile: UserProfile


class UpsertProfileUseCase:
    def __init__(self, uow: UsersUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, cmd: UpsertProfileCommand) -> UpsertProfileResult:
        async with self._uow as uow:
            profile = await uow.profiles.get_by_user_id(cmd.user_id)
            if profile is None:
                profile = UserProfile(
                    user_id=cmd.user_id,
                    username=cmd.username,
                    first_name=cmd.first_name,
                    last_name=cmd.last_name,
                    birthday=cmd.birthday,
                    photo_url=cmd.photo_url,
                )
                await uow.profiles.add(profile)
            else:
                profile.update_profile(
                    username=cmd.username,
                    first_name=cmd.first_name,
                    last_name=cmd.last_name,
                    birthday=cmd.birthday,
                    photo_url=cmd.photo_url,
                )
                await uow.profiles.update(profile)

            await uow.commit()

        return UpsertProfileResult(profile=profile)
