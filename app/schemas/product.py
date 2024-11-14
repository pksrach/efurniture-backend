from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductPriceRequest(BaseModel):
    color_id: UUID
    size: str = None
    price: float = 0.0


class ProductRequest(BaseModel):
    name: str | UUID = Field(default="Table Set")
    description: str = None
    attachment: Optional[str] = None
    category_id: UUID | str
    brand_id: UUID | str
    product_prices: list[ProductPriceRequest] = None
