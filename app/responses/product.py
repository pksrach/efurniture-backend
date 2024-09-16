from uuid import UUID

from pydantic import BaseModel

from app.models.product import Product
from app.responses.base import BaseResponse


class KeyValueResponse(BaseModel):
    key: str | UUID
    value: str


class ProductDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None
    category: KeyValueResponse | None
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
                key=product.category.id if product.category else None,
                value=product.category.name if product.category else None,
            ),
            brand=KeyValueResponse(
                key=product.brand.id if product.brand else None,
                value=product.brand.name if product.brand else None,
            ),
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


