from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.brand import Brand
from app.responses.brand import BrandDataResponse, BrandResponse
from app.responses.paginated_response import PaginationParam
from app.schemas.brand import BrandRequest
from app.services.base_service import fetch_paginated_data


async def get_brands(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=Brand,
        pagination=pagination,
        data_response_model=BrandDataResponse,
        order_by_field=Brand.created_at,
        message="Brands fetched successfully"
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
