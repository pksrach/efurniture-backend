from uuid import UUID

from pydantic import BaseModel

from app.models.order_detail import OrderDetail
from app.responses.base import BaseResponse
from app.responses.key_value_response import KeyValueResponse


class OrderDetailDataResponse(BaseModel):
    id: UUID | str
    order_id: UUID | str
    product: KeyValueResponse
    category: KeyValueResponse
    brand: KeyValueResponse
    color: KeyValueResponse
    size: str
    price: float
    qty: int
    total: float

    @classmethod
    def from_entity(cls, order_detail: 'OrderDetail') -> 'OrderDetailDataResponse':
        return cls(
            id=order_detail.id,
            order_id=order_detail.order_id,
            product=KeyValueResponse(
                key=str(order_detail.product_id),
                value=order_detail.product.name if order_detail.product else None
            ),
            category=KeyValueResponse(
                key=str(order_detail.category_id),
                value=order_detail.category.name if order_detail.category else None
            ),
            brand=KeyValueResponse(
                key=str(order_detail.brand_id),
                value=order_detail.brand.name if order_detail.brand else None
            ),
            color=KeyValueResponse(
                key=str(order_detail.color_id),
                value=order_detail.color.name if order_detail.color else None
            ),
            size=order_detail.size,
            price=order_detail.price,
            qty=order_detail.qty,
            total=order_detail.total
        )


class OrderDetailResponse(BaseResponse):
    data: OrderDetailDataResponse | None

    @classmethod
    def from_entity(cls, order_detail: 'OrderDetail') -> 'OrderDetailResponse':
        return cls(
            data=OrderDetailDataResponse.from_entity(order_detail),
            message="Order detail fetched successfully"
        )


class OrderDetailListResponse(BaseResponse):
    data: list[OrderDetailDataResponse]

    @classmethod
    def from_entities(cls, order_details: list['OrderDetail']) -> 'OrderDetailListResponse':
        return cls(
            data=[OrderDetailDataResponse.from_entity(order_detail) for order_detail in order_details],
            message="Order details fetched successfully"
        )
