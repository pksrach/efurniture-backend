from typing import TypeVar, Generic, List
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]         # List of generic type T (data items)
    message: str          # A message indicating the status
    page: int             # Current page number
    limit: int            # Number of items per page (page size)
    total_items: int      # Total number of items in the database
    total_pages: int      # Total number of pages

    class Config:
        orm_mode = True   # Enable compatibility with ORM models
