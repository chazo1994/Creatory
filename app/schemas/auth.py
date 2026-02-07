from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import UserPublic


class PasswordMixin(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(PasswordMixin):
    email: EmailStr
    display_name: str | None = Field(default=None, max_length=120)


class LoginRequest(PasswordMixin):
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthResponse(BaseModel):
    token: TokenResponse
    user: UserPublic
