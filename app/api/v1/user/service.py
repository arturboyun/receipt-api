from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.schemes import UserCreateSchema
from app.api.v1.auth.utils import SecurityManager
from app.api.v1.user.models import User
from app.core.crud_service import CrudService
from app.core.repository import Repository


class UserService(CrudService[User, UserCreateSchema]):
    def __init__(self, repository: Repository[User, AsyncSession], security_manager: SecurityManager):
        super().__init__(repository)
        self.security_manager = security_manager

    async def create(self, session: AsyncSession, data: UserCreateSchema, creator_id: int) -> T:
        data = data.model_dump()
        data["password"] = self.security_manager.get_password_hash(data["password"])
        return await self.repository.create(session, data)
