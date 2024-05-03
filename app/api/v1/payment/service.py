from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.payment.models import Payment
from app.api.v1.payment.schemes import PaymentSchema
from app.core.crud_service import CrudService
from app.core.repository import Repository


class PaymentService(CrudService[Payment, PaymentSchema]):
    def __init__(self, repository: Repository[Payment, AsyncSession]):
        super().__init__(repository)
