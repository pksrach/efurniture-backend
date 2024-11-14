from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class OrderDetailRequest(BaseModel):
    product_id: UUID
    color_id: Optional[UUID]
    size: Optional[str]
    category_id: Optional[UUID]
    brand_id: Optional[UUID]
    price: float
    qty: int


class OrderRequest(BaseModel):
    location_id: UUID | str
    payment_method_id: UUID
    payment_attachment: str
    note: Optional[str] | None
    details: List[OrderDetailRequest]
