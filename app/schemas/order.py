from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class OrderDetailRequest(BaseModel):
    product_id: UUID
    product_price_id: UUID
    product_name: str
    color_id: Optional[UUID]
    color_name: Optional[str]
    size: Optional[str]
    category_id: Optional[UUID]
    category_name: Optional[str]
    brand_id: Optional[UUID]
    brand_name: Optional[str]
    price: float
    qty: int


class OrderRequest(BaseModel):
    order_date: datetime
    location_id: UUID
    payment_method_id: UUID
    payment_attachment: str
    note: Optional[str] | None
    details: List[OrderDetailRequest]
