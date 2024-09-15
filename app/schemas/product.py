from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ProductRequest(BaseModel):
    name: str = Field(default="Table Set")
    description: str = None
    attachment: Optional[str] = None
    category_id: UUID
    brand_id: UUID
