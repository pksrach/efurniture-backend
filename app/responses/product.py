from uuid import UUID

from pydantic import BaseModel

from app.models.product import Product
from app.responses.base import BaseResponse
from app.responses.key_value_response import KeyValueResponse
from app.responses.product_price_response import ProductPriceDataResponse


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


class ProductResponseWithoutProductPrice(BaseResponse):
    data: ProductDataResponse | None

    @classmethod
    def from_entity(cls, product: 'Product') -> 'ProductResponseWithoutProductPrice':
        return cls(
            data=ProductDataResponse(
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
                product_prices=None,
                is_active=product.is_active,
            ),
            message="Product fetched successfully"
        )
