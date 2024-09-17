from uuid import UUID
from pydantic import BaseModel

from app.models.payment_method import PaymentMethod
from app.responses.base import BaseResponse


class PaymentMethodDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    type: str
    is_active: bool
    transaction_fee: float
    currency: str
    provider: str | None
    attachment_qr: str | None

    @classmethod
    def from_entity(cls, payment_method: 'PaymentMethod') -> 'PaymentMethodDataResponse':
        if payment_method is None:
            return cls(
                id="",
                name="",
                description=None,
                type="",
                is_active=False,
                transaction_fee=0.0,
                currency="",
                provider=None,
                attachment_qr=None
            )

        return cls(
            id=payment_method.id,
            name=payment_method.name,
            description=payment_method.description,
            type=payment_method.type,
            is_active=payment_method.is_active,
            transaction_fee=payment_method.transaction_fee,
            currency=payment_method.currency,
            provider=payment_method.provider,
            attachment_qr=payment_method.attachment_qr
        )


class PaymentMethodResponse(BaseResponse):
    data: PaymentMethodDataResponse | None

    @classmethod
    def from_entity(cls, payment_method: 'PaymentMethod') -> 'PaymentMethodResponse':
        if payment_method is None:
            return cls(
                data=None,
                message="Payment method not found"
            )

        return cls(
            data=PaymentMethodDataResponse.from_entity(payment_method),
            message="Payment method fetched successfully"
        )


class PaymentMethodListResponse(BaseResponse):
    data: list[PaymentMethodDataResponse]

    @classmethod
    def from_entities(cls, payment_methods: list['PaymentMethod']) -> 'PaymentMethodListResponse':
        return cls(
            data=[PaymentMethodDataResponse.from_entity(pm) for pm in payment_methods],
            message="Payment methods fetched successfully"
        )
