from uuid import UUID

from pydantic import BaseModel

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


class ProductResponse(BaseResponse):
    data: ProductDataResponse | None


class ProductListResponse(BaseResponse):
    data: list[ProductDataResponse]
