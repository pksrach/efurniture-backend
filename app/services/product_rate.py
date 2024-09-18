from sqlalchemy.exc import IntegrityError
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.product_rate import ProductRate
from app.responses.paginated_response import PaginatedResponse
from app.schemas.product_rate import ProductRateRequest
from app.responses.product_rate import ProductRate, ProductRateDataResponse,ProductRateListResponse,ProductRateResponse
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

async def _get_product_rate_by_id(id: str, session: AsyncSession) -> Optional[ProductRate]:
    stmt = select(ProductRate).where(ProductRate.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_product_rates(session: AsyncSession) -> ProductRateListResponse:
    stmt = select(ProductRate).order_by(ProductRate.created_at.desc())
    result = await session.execute(stmt)
    product_rates = result.scalars().all()
    return ProductRateListResponse.from_entities(list(product_rates))

async def get_paginated_product_rates(session: AsyncSession, page: int = 1, limit: int = 10)-> PaginatedResponse[ProductRateDataResponse]:
    offset = (page - 1) * limit
    total_items_query = await session.execute(select(func.count(ProductRate.id)))
    total_items = total_items_query.scalar_one()
    stmt = select(ProductRate).order_by(ProductRate.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    product_rates = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    product_rate_data = [ProductRateDataResponse.from_entity(product_rate) for product_rate in product_rates]

    return PaginatedResponse[ProductRateDataResponse](
        data=product_rate_data,
        message="Product Rates retrieved successfully.",
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )

async def get_product_rate(id: str, session: AsyncSession) -> ProductRateResponse:
    product_rate = await _get_product_rate_by_id(id, session)

    if product_rate is None:
        logger.warning(f"Product Rate with ID {id} not found.")
        return ProductRateResponse(
            data=None,
            message="Product Rate not found"
        )
    return ProductRateResponse.from_entity(product_rate)

async def create_product_rate(req: ProductRateRequest, session: AsyncSession) -> ProductRateResponse:
    """Create a new Product Rate with the provided data."""
    # Optionally check if a Product Rate with the same name exists
    product_rate = ProductRate(
        user_id = req.user_id,
        product_id = req.product_id,
        rate = req.rate
    )

    try:
        session.add(product_rate)
        await session.commit()
        await session.refresh(product_rate)
        logger.info(f"Product Rate created successfully.")
        return ProductRateResponse(
            data=ProductRateDataResponse.from_entity(product_rate),
            message="Product Rate created successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during creation of Product Rate: {str(e)}")
        return ProductRateResponse(
            data=None,
            message="Failed to create Product Rate due to database integrity error."
        )

async def update_product_rate(id: str, req: ProductRateRequest, session: AsyncSession) -> ProductRateResponse:
    """Update a Product Rate by ID with the provided data."""
    product_rate = await _get_product_rate_by_id(id, session)

    if product_rate is None:
        logger.warning(f"Product Rate with ID {id} not found.")
        return ProductRateResponse(
            data=None,
            message="Product Rate not found"
        )

    update_data = req.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product_rate, key, value)

    try:
        await session.commit()
        await session.refresh(product_rate)
        logger.info(f"Product Rate with ID {id} updated successfully.")
        return ProductRateResponse(
            data=ProductRateDataResponse.from_entity(product_rate),
            message="Product Rate updated successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during update of Product Rate {id}: {str(e)}")
        return ProductRateResponse(
            data=None,
            message="Failed to update Product Rate due to database integrity error."
        )

async def delete_product_rate(id: str, session: AsyncSession)-> ProductRateResponse:
    stmt = select(ProductRate).where(ProductRate.id == id)
    result = await session.execute(stmt)
    product_rate = result.scalar()

    if product_rate is None:
        return ProductRateResponse(
            data=None,
            message="Product Rate not found"
        )
    
    await session.delete(product_rate)
    await session.commit()
    return ProductRateResponse(
        data=ProductRateDataResponse.from_entity(product_rate),
        message="Product Rate deleted successfully"
    )