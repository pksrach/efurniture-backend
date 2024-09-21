import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.paginated_response import PaginationParam
from app.responses.payment_method import PaymentMethod, PaymentMethodDataResponse, PaymentMethodResponse
from app.schemas.payment_method import PaymentMethodRequest
from app.services.base_service import fetch_paginated_data

logger = logging.getLogger(__name__)


async def _get_payment_method_by_id(id: str, session: AsyncSession) -> Optional[PaymentMethod]:
    stmt = select(PaymentMethod).where(PaymentMethod.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_payment_methods(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=PaymentMethod,
        pagination=pagination,
        data_response_model=PaymentMethodDataResponse,
        order_by_field=PaymentMethod.created_at,
        message="Payment methods fetched successfully"
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


async def delete_payment_method(id: str, session: AsyncSession) -> PaymentMethodResponse:
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
