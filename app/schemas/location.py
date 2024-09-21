from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

class LocationRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    parent_id: Optional[UUID] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "New York",
                "price": 150.00,
                "parent_id": "bdea8a6c-3d58-4e57-9fbf-efdbd647f6e4"
            }
        }
