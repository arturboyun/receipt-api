from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

from app.api.v1.payment.constants import PaymentTypeEnum


class PaymentSchema(BaseModel):
    type: PaymentTypeEnum
    amount: Decimal = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)


class PaymentSchemaResponse(PaymentSchema):
    amount: float

    model_config = ConfigDict(from_attributes=True)
