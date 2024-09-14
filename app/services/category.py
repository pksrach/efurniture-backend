from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.category import Category
from app.responses.category import CategoryListResponse, CategoryDataResponse, CategoryResponse
from app.schemas.category import CategoryRequest

settings = get_settings()


async def get_categories(session: AsyncSession) -> CategoryListResponse:
    stmt = select(Category).order_by(Category.created_at.desc())
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return CategoryListResponse(
        data=[CategoryDataResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        ) for category in categories],
        message="Categories fetched successfully"
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

    return CategoryResponse(
        data=CategoryDataResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        ),
        message="Category fetched successfully"
    )


async def create_category(req: CategoryRequest, session: AsyncSession) -> CategoryResponse:
    # Check exists name or not
    stmt = select(Category).where(Category.name == req.name)
    result = await session.execute(stmt)
    category = result.scalars().first()
    if category:
        return CategoryResponse(
            data=CategoryDataResponse(
                id=category.id,
                name=category.name,
                description=category.description,
                attachment=category.attachment
            ),
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
        data=CategoryDataResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        ),
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
        data=CategoryDataResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        ),
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
        data=CategoryDataResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            attachment=category.attachment
        ),
        message="Category deleted successfully"
    )
