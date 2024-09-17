from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class ProductRateRequest(BaseModel):
    user_id: Optional[UUID] = None
    product_id: Optional[UUID] = None
    rate: Optional[int] = Field(None, ge=1, le=5)  # Assuming a 1-5 rating scale

