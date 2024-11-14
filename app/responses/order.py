from datetime import date
from uuid import UUID

from pydantic import BaseModel

from app.models.order import Order
from app.responses.base import BaseResponse
from app.responses.key_value_response import KeyValueResponse


class OrderDataResponse(BaseModel):
    id: UUID | str
    order_date: date
    customer: KeyValueResponse
    location: KeyValueResponse
    location_price: float
    amount: float
    payment_method: KeyValueResponse
    payment_attachment: str | None
    order_status: str
    note: str | None
    staff: KeyValueResponse | None

    @classmethod
    def from_entity(cls, order: 'Order') -> 'OrderDataResponse':
        return cls(
            id=order.id,
            order_date=order.order_date,
            customer=KeyValueResponse(
                key=str(order.customer_id),
                value=order.customer.name if order.customer else None
            ),
            location=KeyValueResponse(
                key=str(order.location_id),
                value=order.location.name if order.location else None
            ),
            location_price=order.location_price,
            amount=order.amount,
            payment_method=KeyValueResponse(
                key=str(order.payment_method_id),
                value=order.payment_method.name if order.payment_method else None
            ),
            payment_attachment=order.payment_attachment,
            order_status=order.order_status,
            note=order.note,
            staff=KeyValueResponse(
                key=str(order.staff_id),
                value=order.staff.name if order.staff else None
            ) if order.staff else None
        )


class OrderResponse(BaseResponse):
    data: OrderDataResponse | None

    @classmethod
    def from_entity(cls, order: 'Order') -> 'OrderResponse':
        return cls(
            data=OrderDataResponse.from_entity(order),
            message="Order fetched successfully"
        )


class OrderListResponse(BaseResponse):
    data: list[OrderDataResponse]

    @classmethod
    def from_entities(cls, orders: list['Order']) -> 'OrderListResponse':
        return cls(
            data=[OrderDataResponse.from_entity(order) for order in orders],
            message="Orders fetched successfully"
        )