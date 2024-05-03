from decimal import Decimal
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud_service import CrudService
from app.core.repository import Repository
from .models import Receipt
from .schemes import ReceiptCreateSchema, ReceiptResponseSchema, ProductCreateSchema, PaymentSchema
from ..payment.service import PaymentService


class ReceiptService(CrudService[Receipt, ReceiptCreateSchema]):
    def __init__(self, repository: Repository[Receipt, AsyncSession], payment_service: PaymentService):
        super().__init__(repository)
        self.payment_service = payment_service

    async def create(self, session: AsyncSession, data: ReceiptCreateSchema, creator_id: int) -> Receipt:
        data = data.model_dump()
        data["user_id"] = creator_id

        payment = await self.payment_service.create(session, PaymentSchema(**data.pop("payment")), creator_id)
        data["payment_id"] = payment.id

        data["products"] = self._calculate_total_for_products(data["products"])
        data["total"] = self._calculate_total_for_receipt(data["products"])
        data["rest"] = self._calculate_rest(data["total"], payment.amount)

        if data["rest"] < 0:
            raise HTTPException(status_code=400, detail="Payment amount is less than total")

        receipt = await self.repository.create(session, data)
        return receipt

    def _calculate_rest(self, total: Decimal, payment: Decimal) -> Decimal:
        return Decimal(payment - total)

    def _calculate_total_for_products(self, products: list[ProductCreateSchema]) -> Sequence[dict]:
        return [{**product, "total": product["price"] * product["quantity"]} for product in products]

    def _calculate_total_for_receipt(self, products: list[ProductCreateSchema]) -> Decimal:
        return Decimal(sum([product["total"] for product in products]))
