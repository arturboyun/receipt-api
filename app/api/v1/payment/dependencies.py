from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.repository import Repository
from .models import Payment
from .repositories import PaymentRepository
from .service import PaymentService


async def get_payment_repository() -> Repository[Payment, AsyncSession]:
    return PaymentRepository()


async def get_payment_service(
    repository: Annotated[Repository[Payment, AsyncSession], Depends(get_payment_repository)]
) -> PaymentService:
    return PaymentService(repository)
