from typing import List, Union, TypeVar, Optional

from sqlalchemy import select, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.base import BaseResponse
from app.responses.paginated_response import PaginatedResponse, PaginationParam

T = TypeVar("T")


async def fetch_paginated_data(
        session: AsyncSession,
        stmt: Optional[select] = None,
        entity=None,
        pagination: PaginationParam = PaginationParam(),
        data_response_model=None,
        order_by_field=None,
        message: str = "Data fetched successfully",
) -> Union[PaginatedResponse, BaseResponse, List[T]]:
    """
    Fetch data with pagination or without pagination based on the `pagination.is_page` flag.

    Args:
        session: The async SQLAlchemy session
        entity: The ORM entity model class (e.g., Category)
        pagination: Pagination parameters
        data_response_model: The Pydantic model for the data response
        order_by_field: Field to order the data by (e.g., entity.created_at)

    Returns:
        PaginatedResponse or BaseResponse or List of data response model
        :param session:
        :param stmt:
        :param entity:
        :param pagination:
        :param data_response_model:
        :param order_by_field:
        :param message:
    """
    # Create the base query if stmt is not provided
    if stmt is None:
        stmt = select(entity)
    else:
        stmt = stmt

    # Apply search filter if provided
    if pagination.search:
        search_term = pagination.search.split(":")
        if len(search_term) == 2:
            field, value = search_term
            search_value = f"%{value}%"
            if hasattr(entity, field):
                stmt = stmt.where(getattr(entity, field).ilike(search_value))
        else:
            search_value = f"%{pagination.search}%"
            stmt = stmt.where(
                (cast(entity.id, String).ilike(search_value)) | (entity.name.ilike(search_value))
            )

    # Apply sorting
    if pagination.sort:
        sort_term = pagination.sort.split(":")
        if len(sort_term) == 2:
            field, direction = sort_term
        else:
            field, direction = pagination.sort, "desc"

        sort_field = getattr(entity, field, order_by_field)
        if direction.lower() == "asc":
            stmt = stmt.order_by(sort_field.asc())
        else:
            stmt = stmt.order_by(sort_field.desc())

    if pagination.is_page:
        # Calculate pagination details
        offset = (pagination.page - 1) * pagination.limit
        total_items_query = await session.execute(select(func.count()).select_from(stmt.subquery()))
        total_items = total_items_query.scalar_one()

        # Fetch paginated results
        stmt = stmt.offset(offset).limit(pagination.limit)
        result = await session.execute(stmt)
        entities = result.scalars().all()

        # Calculate total pages
        total_pages = (total_items + pagination.limit - 1) // pagination.limit
        data = [data_response_model.from_entity(item) for item in entities]

        return PaginatedResponse(
            data=data,
            page=pagination.page,
            limit=pagination.limit,
            total_items=total_items,
            total_pages=total_pages,
            message=message
        )
    else:
        # Fetch all data without pagination
        result = await session.execute(stmt)
        entities = result.scalars().all()

        return BaseResponse(
            data=[data_response_model.from_entity(item) for item in entities],
            message=message
        )