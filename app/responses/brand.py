from uuid import UUID

from pydantic import BaseModel

from app.responses.base import BaseResponse


class BrandDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None


class BrandResponse(BaseResponse):
    data: BrandDataResponse | None


class BrandListResponse(BaseResponse):
    data: list[BrandDataResponse]
