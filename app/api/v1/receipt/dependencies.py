from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.payment.dependencies import get_payment_service
from app.core.repository import Repository
from .models import Receipt
from .repositories import ReceiptRepository
from .services import ReceiptService
from ..payment.service import PaymentService


async def get_receipt_repository() -> Repository[Receipt, AsyncSession]:
    return ReceiptRepository()


async def get_receipt_service(
    repository: Annotated[Repository[Receipt, AsyncSession], Depends(get_receipt_repository)],
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
) -> ReceiptService:
    return ReceiptService(repository, payment_service)
