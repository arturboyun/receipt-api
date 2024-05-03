from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository import Repository
from .models import User
from .repositories import UserRepository


async def get_user_repository() -> Repository[User, AsyncSession]:
    return UserRepository()
