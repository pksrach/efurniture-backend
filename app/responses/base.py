from pydantic import BaseModel, ConfigDict


class BaseResponse(BaseModel):
    message: str = "fetched successfully"
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)
