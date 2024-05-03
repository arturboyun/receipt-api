import datetime

from fastapi_filter.contrib.sqlalchemy import Filter

from app.api.v1.payment.constants import PaymentTypeEnum
from app.api.v1.payment.models import Payment


class PaymentFilter(Filter):
    type: PaymentTypeEnum | None = None
    type__ilike: str | None = None
    type__like: str | None = None
    type__neq: str | None = None
    created_at__lt: datetime.datetime | None = None
    created_at__lte: datetime.datetime | None = None
    created_at__gt: datetime.datetime | None = None

    class Constants(Filter.Constants):
        model = Payment
