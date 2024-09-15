from typing import Optional

from pydantic import BaseModel, Field


class ColorRequest(BaseModel):
    code: str = Field(default="#FF0000")
    name: str = Field(default="Red")
    highlight: Optional[str] = None
