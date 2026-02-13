from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from creatory_core.api.deps import get_current_user
from creatory_core.core.config import settings
from creatory_core.core.security import create_access_token, get_password_hash, verify_password
from creatory_core.db.models import User
from creatory_core.db.session import get_db_session
from creatory_core.schemas.auth import AuthResponse, LoginRequest, RegisterRequest, TokenResponse
from creatory_core.schemas.common import UserPublic

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    existing = await db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email.lower(),
        password_hash=get_password_hash(payload.password),
        display_name=payload.display_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    return AuthResponse(
        token=TokenResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
        ),
        user=UserPublic.model_validate(user),
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    payload: LoginRequest,
    db: AsyncSession = Depends(get_db_session),
) -> AuthResponse:
    user = await db.scalar(select(User).where(User.email == payload.email.lower()))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )

    return AuthResponse(
        token=TokenResponse(
            access_token=token,
            expires_in=settings.access_token_expire_minutes * 60,
        ),
        user=UserPublic.model_validate(user),
    )


@router.post("/token", response_model=TokenResponse)
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db_session),
) -> TokenResponse:
    user = await db.scalar(select(User).where(User.email == form_data.username.lower()))
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
    )


@router.get("/me", response_model=UserPublic)
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)
