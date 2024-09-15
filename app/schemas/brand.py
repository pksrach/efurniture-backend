from typing import Optional

from pydantic import BaseModel, Field


class BrandRequest(BaseModel):
    name: str = Field(default="Honda")
    description: Optional[str] = None
    attachment: Optional[str] = None
