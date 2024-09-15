from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.brand import Brand
from app.responses.brand import BrandListResponse, BrandDataResponse, BrandResponse
from app.schemas.brand import BrandRequest

settings = get_settings()


async def get_brands(session: AsyncSession) -> BrandListResponse:
    stmt = select(Brand).order_by(Brand.created_at.desc())
    result = await session.execute(stmt)
    brands = result.scalars().all()
    return BrandListResponse(
        data=[BrandDataResponse(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        ) for brand in brands],
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

    return BrandResponse(
        data=BrandDataResponse(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        ),
        message="Brand fetched successfully"
    )


async def create_brand(req: BrandRequest, session: AsyncSession) -> BrandResponse:
    # Check exists name or not
    stmt = select(Brand).where(Brand.name == req.name)
    result = await session.execute(stmt)
    brand = result.scalars().first()
    if brand:
        return BrandResponse(
            data=BrandDataResponse(
                id=brand.id,
                name=brand.name,
                description=brand.description,
                attachment=brand.attachment
            ),
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
        data=BrandDataResponse(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        ),
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
        data=BrandDataResponse(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        ),
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
        data=BrandDataResponse(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        ),
        message="Brand deleted successfully"
    )
