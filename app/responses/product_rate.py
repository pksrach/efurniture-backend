from uuid import UUID
from pydantic import BaseModel

from app.models.product_rate import ProductRate
from app.responses.base import BaseResponse


class ProductRateDataResponse(BaseModel):
    user_id: str | UUID
    product_id: str | UUID
    rate: int

    @classmethod
    def from_entity(cls, product_rate: 'ProductRate') -> 'ProductRateDataResponse':
        if product_rate is None:
            return cls(
                user_id="",
                product_id="",
                rate=0
            )

        return cls(
            user_id=product_rate.user_id,
            product_id=product_rate.product_id,
            rate=product_rate.rate
        )


class ProductRateResponse(BaseResponse):
    data: ProductRateDataResponse | None

    @classmethod
    def from_entity(cls, product_rate: 'ProductRate') -> 'ProductRateResponse':
        if product_rate is None:
            return cls(
                data=None,
                message="Product rate not found"
            )

        return cls(
            data=ProductRateDataResponse.from_entity(product_rate),
            message="Product rate fetched successfully"
        )


class ProductRateListResponse(BaseResponse):
    data: list[ProductRateDataResponse]

    @classmethod
    def from_entities(cls, product_rates: list['ProductRate']) -> 'ProductRateListResponse':
        return cls(
            data=[ProductRateDataResponse.from_entity(pr) for pr in product_rates],
            message="Product rates fetched successfully"
        )
