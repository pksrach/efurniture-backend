from uuid import UUID

from pydantic import BaseModel


class CartRequest(BaseModel):
    product_price_id: UUID | str
    qty: int
