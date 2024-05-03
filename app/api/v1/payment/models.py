from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.v1.payment.constants import PaymentTypeEnum
from app.models import Base

if TYPE_CHECKING:
    from app.api.v1.receipt.models import Receipt


class Payment(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    type: Mapped[PaymentTypeEnum] = mapped_column(Enum(PaymentTypeEnum))
    amount: Mapped[Decimal] = mapped_column()

    receipt: Mapped["Receipt"] = relationship(back_populates="payment")
