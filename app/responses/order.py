from datetime import datetime
from uuid import UUID

import pytz
from pydantic import BaseModel

from app.config.settings import get_settings
from app.models.order import Order
from app.responses.base import BaseResponse
from app.responses.key_value_response import KeyValueResponse


settings = get_settings()

class OrderDataResponse(BaseModel):
    id: UUID | str
    order_date: str
    order_number: str | None
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
        env_timezone = settings.TIMEZONE
        local_tz = pytz.timezone(env_timezone)

        # Ensure created_at is timezone-aware
        if order.order_date.tzinfo is None:
            order.order_date = pytz.utc.localize(order.order_date)

        # Convert to local timezone
        local_dt = order.order_date.astimezone(local_tz)

        return cls(
            id=order.id,
            order_date=local_dt.strftime("%d-%m-%Y %I:%M %p"),
            order_number=order.order_number,
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
