from typing import TypeVar, Generic, List

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    message: str
    page: int
    limit: int
    total_items: int
    total_pages: int
