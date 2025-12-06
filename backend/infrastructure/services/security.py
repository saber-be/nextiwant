from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import bcrypt
import jwt

from backend.application.common.interfaces import AuthToken, PasswordHasher, TokenService
from backend.domain.users.entities import UserId


class BcryptPasswordHasher(PasswordHasher):
    def hash(self, raw_password: str) -> str:
        if not raw_password:
            raise ValueError("Password cannot be empty")
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verify(self, raw_password: str, password_hash: str) -> bool:
        if not password_hash:
            return False
        try:
            return bcrypt.checkpw(raw_password.encode("utf-8"), password_hash.encode("utf-8"))
        except ValueError:
            return False


class JwtTokenService(TokenService):
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expires_minutes: int = 60,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._access_token_expires_minutes = access_token_expires_minutes

    def _encode(self, payload: Dict[str, Any]) -> str:
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_access_token(self, user_id: UserId, expires_delta: timedelta | None = None) -> AuthToken:
        now = datetime.now(timezone.utc)
        if expires_delta is None:
            expires_delta = timedelta(minutes=self._access_token_expires_minutes)
        expires_at = now + expires_delta

        payload: Dict[str, Any] = {
            "sub": str(user_id.value),
            "exp": expires_at,
        }

        token_str = self._encode(payload)
        return AuthToken(access_token=token_str, expires_at=expires_at)
