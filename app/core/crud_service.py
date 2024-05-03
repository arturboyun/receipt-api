from abc import ABC
from typing import Sequence, Callable, Optional

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from .repository import Repository


class CrudService[T, TC: BaseModel](ABC):
    def __init__(self, repository: Repository[T, AsyncSession]):
        self.repository = repository

    async def find(
        self, session: AsyncSession, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> T | None:
        return await self.repository.find(session, limit, offset, filter_func, **filters)

    async def find_all(
        self, session: AsyncSession, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> Sequence[T]:
        return await self.repository.find_all(session, limit, offset, filter_func, **filters)

    async def total(
        self, session: AsyncSession, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> int:
        return await self.repository.total(session, filter_func, **filters)

    async def get_by_pk(self, session: AsyncSession, pk: int) -> T | None:
        return await self.repository.get_by_pk(session, pk)

    async def create(self, session: AsyncSession, data: TC, creator_id: int | None) -> T:
        return await self.repository.create(session, data.model_dump())

    async def update(self, session: AsyncSession, pk: int, data: TC) -> T:
        return await self.repository.update(session, pk, data.model_dump())

    async def delete(self, session: AsyncSession, pk: int) -> None:
        return await self.repository.delete(session, pk)
