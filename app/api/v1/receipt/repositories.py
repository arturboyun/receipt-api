from typing import Sequence, Optional, Callable

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.core.repository import Repository
from .models import Receipt, Product
from ..payment.models import Payment


class ReceiptRepository(Repository[Receipt, AsyncSession]):
    options = (joinedload(Receipt.products), joinedload(Receipt.payment))

    async def find(
        self, session: AsyncSession, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> Receipt | None:
        stmt = select(Receipt).join(Payment).filter_by(**filters).options(*self.options)
        if filter_func:
            stmt = filter_func(stmt)
        result = await session.execute(stmt.limit(limit).offset(offset))
        return result.scalars().first()

    async def find_all(
        self, session: AsyncSession, limit: int = 10, offset: int = 0, filter_func: Optional[Callable] = None, **filters
    ) -> Sequence[Receipt]:
        stmt = select(Receipt).join(Payment, Receipt.payment_id == Payment.id).options(*self.options)
        if filter_func:
            stmt = filter_func(stmt)
        result = await session.execute(stmt.limit(limit).offset(offset).order_by(Receipt.created_at.desc()))
        return result.unique().scalars().all()

    async def total(self, session: AsyncSession, filter_func: Optional[Callable] = None, **filters) -> int:
        stmt = select(func.count()).select_from(Receipt).join(Payment, Receipt.payment_id == Payment.id)
        if filter_func:
            stmt = filter_func(stmt)
        result = await session.execute(stmt)
        return result.scalar()

    async def get_by_pk(self, session: AsyncSession, pk: int) -> Receipt | None:
        result = await session.execute(select(Receipt).filter_by(id=pk).options(*self.options))
        return result.scalars().first()

    async def create(self, session: AsyncSession, data: dict) -> Receipt:
        products = data.pop("products")
        receipt = Receipt(**data)
        for product in products:
            receipt.products.append(Product(**product))
        session.add(receipt)
        await session.commit()
        await session.refresh(receipt)
        return receipt

    async def update(self, session: AsyncSession, pk: int, data: dict) -> Receipt:
        result = await self.get_by_pk(session, pk)
        for key, value in data.items():
            setattr(result, key, value)
        await session.commit()
        return result

    async def delete(self, session: AsyncSession, pk: int) -> None:
        result = await self.get_by_pk(session, pk)
        await session.delete(result)
        await session.commit()
