from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository import Repository
from .models import User


class UserRepository(Repository[User, AsyncSession]):

    async def find(self, session: AsyncSession, **filters) -> User | None:
        result = await session.execute(select(User).filter_by(**filters))
        return result.scalars().first()

    async def find_all(self, session: AsyncSession, **filters) -> Sequence[User]:
        result = await session.execute(select(User).filter_by(**filters))
        return result.scalars().all()

    async def total(self, session: AsyncSession, **filters) -> int:
        result = await session.execute(select(func.count()).select_from(User).filter_by(**filters))
        return result.scalar()

    async def get_by_pk(self, session: AsyncSession, pk: int) -> User | None:
        result = await session.execute(select(User).filter_by(id=pk))
        return result.scalars().first()

    async def create(self, session: AsyncSession, data: dict) -> User:
        user = User(**data)
        session.add(user)
        await session.commit()
        return user

    async def update(self, session: AsyncSession, pk: int, data: dict) -> User:
        result = await session.execute(select(User).filter_by(id=pk))
        user = result.scalars().first()
        for key, value in data.items():
            setattr(user, key, value)
        await session.commit()
        return user

    async def delete(self, session: AsyncSession, pk: int) -> None:
        result = await session.execute(select(User).filter_by(id=pk))
        user = result.scalars().first()
        await session.delete(user)
        await session.commit()
