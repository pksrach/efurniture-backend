from uuid import UUID

from pydantic import BaseModel

from app.models.product import Product
from app.models.product_price import ProductPrice
from app.responses.base import BaseResponse


class KeyValueResponse(BaseModel):
    key: str | UUID | None
    value: str | None


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


class ProductDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None
    category: KeyValueResponse | None
    product_prices: list[ProductPriceDataResponse] | None
    brand: KeyValueResponse | None
    is_active: bool

    @classmethod
    def from_entity(cls, product: 'Product') -> 'ProductDataResponse':
        return cls(
            id=product.id,
            name=product.name,
            description=product.description,
            attachment=product.attachment,
            category=KeyValueResponse(
                key=str(product.category_id),
                value=product.category.name
            ) if product.category else None,
            brand=KeyValueResponse(
                key=str(product.brand_id),
                value=product.brand.name
            ) if product.brand else None,
            product_prices=[
                ProductPriceDataResponse.from_entity(product_price) for product_price in product.product_prices
            ] if product.product_prices else None,
            is_active=product.is_active,
        )


class ProductResponse(BaseResponse):
    data: ProductDataResponse | None

    @classmethod
    def from_entity(cls, product: 'Product') -> 'ProductResponse':
        return cls(
            data=ProductDataResponse.from_entity(product),
            message="Product fetched successfully"
        )


class ProductListResponse(BaseResponse):
    data: list[ProductDataResponse]

    @classmethod
    def from_entities(cls, products: list['Product']) -> 'ProductListResponse':
        return cls(
            data=[ProductDataResponse.from_entity(product) for product in products],
            message="Products fetched successfully"
        )
