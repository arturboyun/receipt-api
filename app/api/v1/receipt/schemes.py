from decimal import Decimal
from typing import Sequence

from pydantic import BaseModel, Field, ConfigDict

from app.api.v1.payment.schemes import PaymentSchema, PaymentSchemaResponse


class ProductBaseSchema(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    quantity: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductCreateSchema(ProductBaseSchema):
    name: str = Field(..., min_length=1, max_length=42)
    price: Decimal = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class ProductSchema(ProductBaseSchema):
    quantity: int
    total: float
    price: float

    model_config = ConfigDict(from_attributes=True)


class ReceiptScheme(BaseModel):
    payment: PaymentSchema | None = None
    products: list[ProductSchema] | None = None


class ReceiptCreateSchema(ReceiptScheme):
    payment: PaymentSchema
    products: list[ProductCreateSchema]


class ReceiptUpdateSchema(ReceiptScheme):
    pass


class ReceiptResponseSchema(ReceiptScheme):
    id: int
    total: float
    rest: float
    payment: PaymentSchemaResponse

    model_config = ConfigDict(from_attributes=True)


class ReceiptPaginateSchema(BaseModel):
    total: int
    items: Sequence[ReceiptResponseSchema]
    limit: int
    offset: int

    model_config = ConfigDict(from_attributes=True)
