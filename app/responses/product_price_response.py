from uuid import UUID

from pydantic import BaseModel

from app.models.product_price import ProductPrice
from app.responses.key_value_response import KeyValueResponse


class ProductPriceDataResponse(BaseModel):
    id: str | UUID
    color: KeyValueResponse | None
    size: str | None
    price: float

    @classmethod
    def from_entity(cls, product_price: 'ProductPrice') -> 'ProductPriceDataResponse':
        return cls(
            id=product_price.id,
            color=KeyValueResponse(
                key=str(product_price.color_id),
                value=product_price.color.name
            ) if product_price.color else None,
            size=product_price.size,
            price=product_price.price,
        )
