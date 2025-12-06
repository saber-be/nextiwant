from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from backend.application.common.interfaces import AuthToken, PasswordHasher, TokenService
from backend.domain.users.entities import User, UserId
from backend.domain.users.repositories import UnitOfWork as UsersUnitOfWork


@dataclass(slots=True)
class SignUpCommand:
    email: str
    password: str


@dataclass(slots=True)
class SignUpResult:
    user: User


class SignUpUseCase:
    def __init__(
        self,
        uow: UsersUnitOfWork,
        password_hasher: PasswordHasher,
    ) -> None:
        self._uow = uow
        self._password_hasher = password_hasher

    async def execute(self, cmd: SignUpCommand) -> SignUpResult:
        async with self._uow as uow:
            existing = await uow.users.get_by_email(cmd.email)
            if existing is not None:
                raise ValueError("Email is already in use")

            password_hash = self._password_hasher.hash(cmd.password)
            user = User(id=UserId.new(), email=cmd.email, password_hash=password_hash)

            await uow.users.add(user)
            await uow.commit()

        return SignUpResult(user=user)


@dataclass(slots=True)
class LoginCommand:
    email: str
    password: str


@dataclass(slots=True)
class LoginResult:
    user: User
    token: AuthToken


class LoginUseCase:
    def __init__(
        self,
        uow: UsersUnitOfWork,
        password_hasher: PasswordHasher,
        token_service: TokenService,
    ) -> None:
        self._uow = uow
        self._password_hasher = password_hasher
        self._token_service = token_service

    async def execute(self, cmd: LoginCommand) -> LoginResult:
        async with self._uow as uow:
            user: Optional[User] = await uow.users.get_by_email(cmd.email)
            if user is None:
                raise ValueError("Invalid credentials")

            if not self._password_hasher.verify(cmd.password, user.password_hash):
                raise ValueError("Invalid credentials")

        token = self._token_service.create_access_token(user.id)
        return LoginResult(user=user, token=token)
