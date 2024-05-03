import datetime

from fastapi_filter import FilterDepends, with_prefix
from fastapi_filter.contrib.sqlalchemy import Filter

from app.api.v1.payment.filters import PaymentFilter
from app.api.v1.receipt.models import Receipt


class ReceiptFilter(Filter):
    created_at__lt: datetime.datetime | None = None
    created_at__lte: datetime.datetime | None = None
    created_at__gt: datetime.datetime | None = None
    created_at__gte: datetime.datetime | None = None
    total__lt: float | None = None
    total__lte: float | None = None
    total__gt: float | None = None
    total__gte: float | None = None
    rest__lt: float | None = None
    rest__lte: float | None = None
    rest__gt: float | None = None
    rest__gte: float | None = None
    payment: PaymentFilter | None = FilterDepends(with_prefix("payment", PaymentFilter))

    class Constants(Filter.Constants):
        model = Receipt
        # search_model_fields = ["name"]
