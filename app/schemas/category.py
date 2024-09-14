from typing import Optional
from pydantic import BaseModel, Field


class CategoryRequest(BaseModel):
    name: str = Field(default="Table")
    description: Optional[str] = None
    attachment: Optional[str] = None
