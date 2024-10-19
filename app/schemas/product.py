from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductPriceRequest(BaseModel):
    color_id: UUID
    size: str = None
    price: float = 0.0


class ProductRequest(BaseModel):
    name: str = Field(default="Table Set")
    description: str = None
    attachment: Optional[str] = None
    category_id: UUID
    brand_id: UUID
    product_prices: list[ProductPriceRequest] = None
