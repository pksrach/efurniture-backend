from typing import TypeVar, Generic, List

from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]  # List of generic type T (data items)
    page: int  # Current page number
    limit: int  # Number of items per page (page size)
    total_items: int  # Total number of items in the database
    total_pages: int  # Total number of pages
    message: str = "Data fetched successfully"

    class Config:
        from_attributes = True  # Enable compatibility with ORM models


class PaginationParam(BaseModel):
    search: str = Field(default="", alias="search")
    sort: str = Field(default="created_at", alias="sort")
    is_page: bool = Field(default=True, alias="is_page")
    page: int = Field(default=1, alias="page")
    limit: int = Field(default=10, alias="limit")
