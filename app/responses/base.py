from typing import TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class BaseResponse(BaseModel):
    data: T | None
    message: str = "fetched successfully"
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
