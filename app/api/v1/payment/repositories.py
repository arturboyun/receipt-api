from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.payment.models import Payment
from app.core.repository import Repository


class PaymentRepository(Repository[Payment, AsyncSession]):

    async def find(self, session: AsyncSession, **filters) -> Payment | None:
        result = await session.execute(select(Payment).filter_by(**filters))
        return result.scalars().first()

    async def find_all(self, session: AsyncSession, **filters) -> Sequence[Payment]:
        result = await session.execute(select(Payment).filter_by(**filters))
        return result.scalars().all()

    async def total(self, session: AsyncSession, **filters) -> int:
        result = await session.execute(select(func.count(Payment.id)).filter_by(**filters))
        return result.scalar()

    async def get_by_pk(self, session: AsyncSession, pk: int) -> Payment | None:
        result = await session.execute(select(Payment).filter_by(id=pk))
        return result.scalars().first()

    async def create(self, session: AsyncSession, data: dict) -> Payment:
        payment = Payment(**data)
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment

    async def update(self, session: AsyncSession, pk: int, data: dict) -> Payment:
        result = await session.execute(select(Payment).filter_by(id=pk))
        user = result.scalars().first()
        for key, value in data.items():
            setattr(user, key, value)
        await session.commit()
        return user

    async def delete(self, session: AsyncSession, pk: int) -> None:
        result = await session.execute(select(Payment).filter_by(id=pk))
        user = result.scalars().first()
        await session.delete(user)
        await session.commit()
