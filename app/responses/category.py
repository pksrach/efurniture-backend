from uuid import UUID

from pydantic import BaseModel

from app.models.category import Category
from app.responses.base import BaseResponse


class CategoryDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None

    @classmethod
    def from_entity(cls, category: 'Category') -> 'CategoryDataResponse':
        if category is None:
            return cls(
                id="",
                name="",
                description="",
                attachment=""
            )

        return cls(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        )


class CategoryResponse(BaseResponse):
    data: CategoryDataResponse | None

    @classmethod
    def from_entity(cls, category: 'Category') -> 'CategoryResponse':
        if category is None:
            return cls(
                data=None,
                message="Category not found"
            )

        return cls(
            data=CategoryDataResponse.from_entity(category),
            message="Category fetched successfully"
        )


class CategoryListResponse(BaseResponse):
    data: list[CategoryDataResponse]

    @classmethod
    def from_entities(cls, categories: list['Category']) -> 'CategoryListResponse':
        return cls(
            data=[CategoryDataResponse.from_entity(category) for category in categories],
            message="Categories fetched successfully"
        )
