from datetime import UTC, datetime, timedelta
from typing import Any

try:
    from jose import JWTError, jwt
except ModuleNotFoundError:  # pragma: no cover - optional in limited local test envs
    JWTError = Exception  # type: ignore[assignment]
    jwt = None

try:
    from passlib.context import CryptContext
except ModuleNotFoundError:  # pragma: no cover - optional in limited local test envs
    class CryptContext:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _ = (args, kwargs)

        def verify(self, plain_password: str, hashed_password: str) -> bool:
            raise RuntimeError(
                "passlib is required for password verification. "
                "Install project dependencies before using auth endpoints."
            )

        def hash(self, password: str) -> str:
            raise RuntimeError(
                "passlib is required for password hashing. "
                "Install project dependencies before using auth endpoints."
            )

from creatory_core.core.config import settings

# bcrypt has a 72-byte limit; bcrypt_sha256 avoids it while remaining compatible.
pwd_context = CryptContext(schemes=["bcrypt_sha256", "bcrypt"], deprecated="auto")


class TokenDecodeError(ValueError):
    """Raised when token decoding fails."""


def _require_jose() -> None:
    if jwt is not None:
        return
    raise RuntimeError(
        "python-jose is required for auth token operations. "
        "Install project dependencies before using auth endpoints."
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    _require_jose()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode: dict[str, Any] = {"sub": subject, "exp": expire}
    assert jwt is not None  # for type checkers
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict[str, Any]:
    _require_jose()
    try:
        assert jwt is not None  # for type checkers
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
    except JWTError as exc:
        raise TokenDecodeError("Invalid token") from exc

    subject = payload.get("sub")
    if not subject:
        raise TokenDecodeError("Token missing subject")
    return payload
