from uuid import UUID

from pydantic import BaseModel

from app.responses.base import BaseResponse


class ColorDataResponse(BaseModel):
    id: str | UUID
    code: str | None
    name: str
    highlight: str | None


class ColorResponse(BaseResponse):
    data: ColorDataResponse | None


class ColorListResponse(BaseResponse):
    data: list[ColorDataResponse]
