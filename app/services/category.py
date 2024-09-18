from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.category import Category
from app.responses.category import CategoryListResponse, CategoryDataResponse, CategoryResponse
from app.responses.paginated_response import PaginatedResponse
from app.schemas.category import CategoryRequest

settings = get_settings()


async def get_categories(session: AsyncSession) -> CategoryListResponse:
    stmt = select(Category).order_by(Category.created_at.desc())
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return CategoryListResponse.from_entities(list(categories))

async def get_paginated_categories(session: AsyncSession, page: int = 1, limit: int = 10)-> PaginatedResponse[CategoryDataResponse]:
    offset = (page - 1) * limit
    total_items_query = await session.execute(select(func.count(Category.id)))
    total_items = total_items_query.scalar_one()
    stmt = select(Category).order_by(Category.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    category_data = [CategoryDataResponse.from_entity(category) for category in categories]

    return PaginatedResponse[CategoryDataResponse](
        data=category_data,
        message="Categories retrieved successfully.",
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )

async def get_category(id: str, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == id)
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


async def update_category(id: str, req: CategoryRequest, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == id)
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


async def delete_category(id: str, session: AsyncSession) -> CategoryResponse:
    stmt = select(Category).where(Category.id == id)
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
