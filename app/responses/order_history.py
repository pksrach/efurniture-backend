from uuid import UUID

import pytz
from pydantic import BaseModel

from app.config.settings import get_settings
from app.models.order_history import OrderHistory
from app.responses.base import BaseResponse

settings = get_settings()


class OrderHistoryDataResponse(BaseModel):
    id: UUID | str
    order_id: UUID | str
    datetime: str
    order_status: str

    @classmethod
    def from_entity(cls, order_history: 'OrderHistory') -> 'OrderHistoryDataResponse':
        env_timezone = settings.TIMEZONE
        local_tz = pytz.timezone(env_timezone)

        # Ensure created_at is timezone-aware
        if order_history.created_at.tzinfo is None:
            order_history.created_at = pytz.utc.localize(order_history.created_at)

        # Convert to local timezone
        local_dt = order_history.created_at.astimezone(local_tz)

        return cls(
            id=order_history.id,
            order_id=order_history.order_id,
            datetime=local_dt.strftime("%d-%m-%Y %I:%M %p"),
            order_status=order_history.order_status.capitalize()
        )


class OrderHistoryResponse(BaseResponse):
    data: OrderHistoryDataResponse | None

    @classmethod
    def from_entity(cls, order_history: 'OrderHistory') -> 'OrderHistoryResponse':
        return cls(
            data=OrderHistoryDataResponse.from_entity(order_history),
            message="Order history fetched successfully"
        )


class OrderListHistoryResponse(BaseResponse):
    data: list[OrderHistoryDataResponse]

    @classmethod
    def from_entities(cls, order_histories: list['OrderHistory']) -> 'OrderListHistoryResponse':
        return cls(
            data=[OrderHistoryDataResponse.from_entity(order_history) for order_history in order_histories],
            message="Order histories fetched successfully"
        )
