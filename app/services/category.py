from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.responses.category import CategoryDataResponse, CategoryResponse
from app.responses.paginated_response import PaginationParam
from app.schemas.category import CategoryRequest
from app.services.base_service import fetch_paginated_data


async def get_categories(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=Category,
        pagination=pagination,
        data_response_model=CategoryDataResponse,
        order_by_field=Category.created_at,
        message="Categories fetched successfully"
    )


async def get_category(category_id: str, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalars().first()

    if category is None:
        return CategoryResponse(
            data=None,
            message="Category not found"
        )

    return CategoryResponse.from_entity(category)


async def create_category(req: CategoryRequest, session: AsyncSession) -> CategoryResponse:
    # Check exists name or not
    stmt = select(Category).where(Category.name == req.name)
    result = await session.execute(stmt)
    category = result.scalar()
    if category:
        return CategoryResponse(
            data=CategoryDataResponse.from_entity(category),
            message="Category already exists"
        )

    category = Category(
        name=req.name,
        description=req.description,
        attachment=req.attachment
    )
    session.add(category)
    await session.commit()
    return CategoryResponse(
        data=CategoryDataResponse.from_entity(category),
        message="Category created successfully"
    )


async def update_category(category_id: str, req: CategoryRequest, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalars().first()

    if category is None:
        return CategoryResponse(
            data=None,
            message="Category not found"
        )

    category.name = req.name
    category.description = req.description
    category.attachment = req.attachment
    await session.commit()
    return CategoryResponse(
        data=CategoryDataResponse.from_entity(category),
        message="Category updated successfully"
    )


async def delete_category(category_id: str, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalars().first()

    if category is None:
        return CategoryResponse(
            data=None,
            message="Category not found"
        )

    await session.delete(category)
    await session.commit()
    return CategoryResponse(
        data=CategoryDataResponse.from_entity(category),
        message="Category deleted successfully"
    )
