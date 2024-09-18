from sqlalchemy.exc import IntegrityError
from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.payment_method import PaymentMethod
from app.responses.paginated_response import PaginatedResponse
from app.schemas.payment_method import PaymentMethodRequest
from app.responses.payment_method import PaymentMethod,PaymentMethodDataResponse,PaymentMethodListResponse,PaymentMethodResponse
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

async def _get_payment_method_by_id(id: str, session: AsyncSession) -> Optional[PaymentMethod]:
    stmt = select(PaymentMethod).where(PaymentMethod.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_payment_methods(session: AsyncSession) -> PaymentMethodListResponse:
    stmt = select(PaymentMethod).order_by(PaymentMethod.created_at.desc())
    result = await session.execute(stmt)
    payment_methods = result.scalars().all()
    return PaymentMethodListResponse.from_entities(list(payment_methods))

async def get_paginated_payment_methods(session: AsyncSession, page: int = 1, limit: int = 10)-> PaginatedResponse[PaymentMethodDataResponse]:
    offset = (page - 1) * limit
    total_items_query = await session.execute(select(func.count(PaymentMethod.id)))
    total_items = total_items_query.scalar_one()
    stmt = select(PaymentMethod).order_by(PaymentMethod.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    payment_methods = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    payment_method_data = [PaymentMethodDataResponse.from_entity(payment_method) for payment_method in payment_methods]

    return PaginatedResponse[PaymentMethodDataResponse](
        data=payment_method_data,
        message="Payment Methods retrieved successfully.",
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )

async def get_payment_method(id: str, session: AsyncSession) -> PaymentMethodResponse:
    payment_method = await _get_payment_method_by_id(id, session)

    if payment_method is None:
        logger.warning(f"Payment method with ID {id} not found.")
        return PaymentMethodResponse(
            data=None,
            message="Payment method not found"
        )
    return PaymentMethodResponse.from_entity(payment_method)

async def create_payment_method(req: PaymentMethodRequest, session: AsyncSession) -> PaymentMethodResponse:
    """Create a new payment method with the provided data."""
    # Optionally check if a payment method with the same name exists
    payment_method = PaymentMethod(
        name=req.name,
        description=req.description,
        type=req.type,
        is_active=req.is_active,
        transaction_fee=req.transaction_fee,
        currency=req.currency,
        provider=req.provider,
        attachment_qr=req.attachment_qr
    )

    try:
        session.add(payment_method)
        await session.commit()
        await session.refresh(payment_method)
        logger.info(f"Payment method '{req.name}' created successfully.")
        return PaymentMethodResponse(
            data=PaymentMethodDataResponse.from_entity(payment_method),
            message="Payment method created successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during creation of payment method: {str(e)}")
        return PaymentMethodResponse(
            data=None,
            message="Failed to create payment method due to database integrity error."
        )

async def update_payment_method(id: str, req: PaymentMethodRequest, session: AsyncSession) -> PaymentMethodResponse:
    """Update a payment method by ID with the provided data."""
    payment_method = await _get_payment_method_by_id(id, session)

    if payment_method is None:
        logger.warning(f"Payment method with ID {id} not found.")
        return PaymentMethodResponse(
            data=None,
            message="Payment method not found"
        )

    update_data = req.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment_method, key, value)

    try:
        await session.commit()
        await session.refresh(payment_method)
        logger.info(f"Payment method with ID {id} updated successfully.")
        return PaymentMethodResponse(
            data=PaymentMethodDataResponse.from_entity(payment_method),
            message="Payment method updated successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during update of payment method {id}: {str(e)}")
        return PaymentMethodResponse(
            data=None,
            message="Failed to update payment method due to database integrity error."
        )

async def delete_payment_method(id: str, session: AsyncSession)-> PaymentMethodResponse:
    stmt = select(PaymentMethod).where(PaymentMethod.id == id)
    result = await session.execute(stmt)
    payment_method = result.scalar()

    if payment_method is None:
        return PaymentMethodResponse(
            data=None,
            message="Payment Method not found"
        )
    
    await session.delete(payment_method)
    await session.commit()
    return PaymentMethodResponse(
        data=PaymentMethodDataResponse.from_entity(payment_method),
        message="Payment Method deleted successfully"
    )