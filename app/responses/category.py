from uuid import UUID

from pydantic import BaseModel

from app.responses.base import BaseResponse


class CategoryDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None


class CategoryResponse(BaseResponse):
    data: CategoryDataResponse | None


class CategoryListResponse(BaseResponse):
    data: list[CategoryDataResponse]
