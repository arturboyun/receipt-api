from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api.v1.payment.models import Payment
from app.api.v1.user.models import User
from app.models import Base


class Receipt(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    total: Mapped[Decimal] = mapped_column()
    rest: Mapped[Decimal] = mapped_column()

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="receipts", lazy="joined")

    payment_id: Mapped[int] = mapped_column(ForeignKey("payment.id"))
    payment: Mapped["Payment"] = relationship(back_populates="receipt", lazy="joined")

    products: Mapped[list["Product"]] = relationship(back_populates="receipt", lazy="joined")


class Product(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column()
    quantity: Mapped[int] = mapped_column()
    total: Mapped[Decimal] = mapped_column()

    receipt_id: Mapped[int] = mapped_column(ForeignKey("receipt.id"))
    receipt: Mapped[Receipt] = relationship(back_populates="products")
