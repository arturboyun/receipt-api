from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Cookie, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.user.models import User
from app.config import settings
from app.dependencies import get_session
from .dependencies import get_auth_service
from .schemes import UserCreateSchema, AccessTokenSchema, UserSchema
from .services import AuthService
from .utils import SecurityManager

router = APIRouter()


@router.post("/register", response_model=AccessTokenSchema, status_code=201)
async def register(
    user: UserCreateSchema,
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
) -> AccessTokenSchema:
    tokens = await auth_service.register(session, user)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        samesite=settings.COOKIES_SAMESITE,
        secure=settings.COOKIES_SECURE,
    )
    return AccessTokenSchema(access_token=tokens.access_token)


@router.post("/token", response_model=AccessTokenSchema)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    response: Response,
) -> AccessTokenSchema:
    tokens = await auth_service.login(session, form_data)
    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite=settings.COOKIES_SAMESITE,
        secure=settings.COOKIES_SECURE,
    )
    return AccessTokenSchema(access_token=tokens.access_token)


@router.get("/me", response_model=UserSchema)
async def get_me(user: User = Depends(SecurityManager.get_current_user)) -> UserSchema:
    return UserSchema(username=user.username, name=user.name)


@router.post("/refresh-token", response_model=AccessTokenSchema)
async def refresh_access_token(
    response: Response,
    session: Annotated[AsyncSession, Depends(get_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> AccessTokenSchema:
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token not found.")

    tokens = await auth_service.refresh(session, refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        samesite=settings.COOKIES_SAMESITE,
        secure=settings.COOKIES_SECURE,
    )
    return AccessTokenSchema(access_token=tokens.access_token)


@router.post("/logout")
async def logout(response: Response) -> None:
    response.delete_cookie(key="refresh_token")
    return
