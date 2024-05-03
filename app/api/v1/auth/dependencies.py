from typing import Annotated

from fastapi import Depends

from app.api.v1.user.dependencies import get_user_repository
from app.api.v1.user.repositories import UserRepository
from .services import AuthService
from .utils import SecurityManager


async def get_auth_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> AuthService:
    return AuthService(user_repository, SecurityManager())
