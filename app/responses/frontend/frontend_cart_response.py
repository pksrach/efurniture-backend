import logging
from uuid import UUID

from pydantic import BaseModel

from app.models.cart import Cart
from app.models.product import Product
from app.models.product_price import ProductPrice
from app.responses.base import BaseResponse
from app.responses.key_value_response import KeyValueResponse

logger = logging.getLogger(__name__)


class FrontendCartDataResponse(BaseModel):
    cart_id: UUID | str
    product_id: UUID | str
    product_price_id: UUID | str
    product_name: str
    price: float
    qty: int
    total: float
    color: KeyValueResponse | None
    size: str
    category: KeyValueResponse | None
    brand: KeyValueResponse | None

    @classmethod
    def from_entity(cls, cart):
        if cart is None:
            return cls(
                cart_id="",
                product_id="",
                product_price_id="",
                product_name="",
                price=0,
                qty=0,
                total=0,
                color=None,
                size="",
                category=None,
                brand=None
            )

        _product_price: ProductPrice = cart.product_price
        _product: Product = cart.product_price.product

        return cls(
            cart_id=cart.id,
            product_id=_product.id,
            product_price_id=_product_price.id,
            product_name=_product.name,
            price=_product_price.price,
            qty=cart.qty,
            total=cart.qty * _product_price.price,
            color=KeyValueResponse(
                key=str(_product_price.color_id),
                value=_product_price.color.name
            ) if _product_price.color else None,
            size=_product_price.size,
            category=KeyValueResponse(
                key=str(_product.category_id),
                value=_product.category.name
            ) if _product.category else None,
            brand=KeyValueResponse(
                key=str(_product.brand_id),
                value=_product.brand.name
            ) if _product.brand else None
        )


class FrontendCartResponse(BaseResponse):
    data: FrontendCartDataResponse | None

    @classmethod
    def from_entity(cls, cart):
        if cart is None:
            return cls(
                data=None,
                message="Cart not found"
            )

        return cls(
            data=FrontendCartDataResponse.from_entity(cart),
            message="Cart fetched successfully"
        )


class FrontendCartListResponse(BaseResponse):
    data: list[FrontendCartDataResponse] | None

    @classmethod
    def from_entity(cls, carts: list['Cart']):
        return cls(
            data=[FrontendCartDataResponse.from_entity(cart) for cart in carts],
            message="Carts fetched successfully"
        )
