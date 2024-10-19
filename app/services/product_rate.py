import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.paginated_response import PaginationParam
from app.responses.product_rate import ProductRate, ProductRateDataResponse, ProductRateResponse
from app.schemas.product_rate import ProductRateRequest
from app.services.base_service import fetch_paginated_data

logger = logging.getLogger(__name__)


async def _get_product_rate_by_id(id: str, session: AsyncSession) -> Optional[ProductRate]:
    stmt = select(ProductRate).where(ProductRate.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_product_rates(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=ProductRate,
        pagination=pagination,
        data_response_model=ProductRateDataResponse,
        order_by_field=ProductRate.created_at,
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
        user_id=req.user_id,
        product_id=req.product_id,
        rate=req.rate
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


async def delete_product_rate(id: str, session: AsyncSession) -> ProductRateResponse:
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
