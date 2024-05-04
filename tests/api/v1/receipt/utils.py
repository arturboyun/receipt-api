import datetime
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.utils import SecurityManager
from app.api.v1.payment.repositories import PaymentRepository
from app.api.v1.payment.service import PaymentService
from app.api.v1.receipt.models import Receipt
from app.api.v1.receipt.repositories import ReceiptRepository
from app.api.v1.receipt.schemes import ReceiptCreateSchema
from app.api.v1.receipt.services import ReceiptService
from app.api.v1.user.models import User
from tests.utils.random_name import random_lower_string


async def create_random_user(session: AsyncSession) -> User:
    security_manager = SecurityManager()
    user = User(
        username=random_lower_string(),
        password=security_manager.get_password_hash(random_lower_string() + "123Aa"),
        name=random_lower_string(),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_random_receipt(
    session: AsyncSession,
    payment_type: str,
    *,
    total: float | Decimal | None = None,
    created_at: datetime.datetime | None = None,
) -> Receipt:
    user = await create_random_user(session)
    owner_id = user.id
    assert owner_id is not None
    payment_service = PaymentService(repository=PaymentRepository())
    receipt_service = ReceiptService(repository=ReceiptRepository(), payment_service=payment_service)
    data = ReceiptCreateSchema.model_validate(
        {
            "payment": {"type": payment_type, "amount": 1000},
            "products": [
                {"name": "test1", "price": 123.0, "quantity": 2, "total": 246.0},
                {"name": "asdf", "price": 21.0, "quantity": 6, "total": 126.0},
            ],
        }
    )
    receipt = await receipt_service.create(session, data, owner_id)

    if created_at:
        receipt.created_at = created_at
    if total:
        receipt.total = total
    await session.commit()
    await session.refresh(receipt)
    return receipt
