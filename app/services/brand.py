from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.brand import Brand
from app.responses.brand import BrandListResponse, BrandDataResponse, BrandResponse
from app.responses.paginated_response import PaginatedResponse
from app.schemas.brand import BrandRequest

settings = get_settings()


async def get_brands(session: AsyncSession) -> BrandListResponse:
    stmt = select(Brand).order_by(Brand.created_at.desc())
    result = await session.execute(stmt)
    brands = result.scalars().all()
    return BrandListResponse.from_entities(list(brands))

async def get_paginated_brands(session: AsyncSession, page: int = 1, limit: int = 10) -> PaginatedResponse[BrandDataResponse]:
    offset = (page - 1) * limit
    total_items_query = await session.execute(select(func.count(Brand.id)))
    total_items = total_items_query.scalar_one()
    stmt = select(Brand).order_by(Brand.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    brands = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    brand_data = [BrandDataResponse.from_entity(brand) for brand in brands]

    return PaginatedResponse[BrandDataResponse](
        data=brand_data,
        message="Brands retrieved successfully.",
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )

async def get_brand(id: str, session: AsyncSession) -> BrandResponse:
    stmt = select(Brand).where(Brand.id == id)
    result = await session.execute(stmt)
    brand = result.scalars().first()

    if brand is None:
        return BrandResponse(
            data=None,
            message="Brand not found"
        )

    return BrandResponse.from_entity(brand)


async def create_brand(req: BrandRequest, session: AsyncSession) -> BrandResponse:
    # Check exists name or not
    stmt = select(Brand).where(Brand.name == req.name)
    result = await session.execute(stmt)
    brand = result.scalar()
    if brand:
        return BrandResponse(
            data=BrandDataResponse.from_entity(brand),
            message="Brand already exists"
        )

    brand = Brand(
        name=req.name,
        description=req.description,
        attachment=req.attachment
    )
    session.add(brand)
    await session.commit()
    return BrandResponse(
        data=BrandDataResponse.from_entity(brand),
        message="Brand created successfully"
    )


async def update_brand(id: str, req: BrandRequest, session: AsyncSession) -> BrandResponse:
    stmt = select(Brand).where(Brand.id == id)
    result = await session.execute(stmt)
    brand = result.scalars().first()

    if brand is None:
        return BrandResponse(
            data=None,
            message="Brand not found"
        )

    brand.name = req.name
    brand.description = req.description
    brand.attachment = req.attachment
    await session.commit()
    return BrandResponse(
        data=BrandDataResponse.from_entity(brand),
        message="Brand updated successfully"
    )


async def delete_brand(id: str, session: AsyncSession) -> BrandResponse:
    stmt = select(Brand).where(Brand.id == id)
    result = await session.execute(stmt)
    brand = result.scalars().first()

    if brand is None:
        return BrandResponse(
            data=None,
            message="Brand not found"
        )

    await session.delete(brand)
    await session.commit()
    return BrandResponse(
        data=BrandDataResponse.from_entity(brand),
        message="Brand deleted successfully"
    )
