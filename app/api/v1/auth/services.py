from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.user.models import User
from app.core.repository import Repository
from .schemes import UserCreateSchema, TokenPairSchema
from .utils import SecurityManager


class AuthService:

    def __init__(self, user_repository: Repository[User, AsyncSession], security_manager: SecurityManager):
        self.user_repository = user_repository
        self.security_manager = security_manager

    async def register(self, session: AsyncSession, user: UserCreateSchema) -> TokenPairSchema:
        if await self.user_repository.find(session, username=user.username):
            raise HTTPException(status_code=400, detail="User with this username already exists")

        user.password = self.security_manager.get_password_hash(user.password)
        user = await self.user_repository.create(session, user.model_dump())

        access_token = self.security_manager.create_access_token(data={"sub": user.username})
        refresh_token = self.security_manager.create_refresh_token(data={"sub": user.username})
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    async def login(self, session: AsyncSession, form_data: OAuth2PasswordRequestForm) -> TokenPairSchema:
        user = await self.user_repository.find(session, username=form_data.username)

        if not user or not self.security_manager.verify_password(form_data.password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")

        access_token = self.security_manager.create_access_token(data={"sub": user.username})
        refresh_token = self.security_manager.create_refresh_token(data={"sub": user.username})
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    async def refresh(self, session: AsyncSession, refresh_token: str) -> TokenPairSchema:
        payload = self.security_manager.decode_token(refresh_token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=400, detail="Invalid token")

        username = payload["sub"]
        user = await self.user_repository.find(session, username=username)
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        access_token = self.security_manager.create_access_token(data={"sub": user.username})
        refresh_token = self.security_manager.create_refresh_token(data={"sub": user.username})
        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)
