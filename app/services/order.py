import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.order import Order
from app.responses.order import OrderDataResponse
from app.responses.paginated_response import PaginationParam
from app.services.base_service import fetch_paginated_data

logger = logging.getLogger(__name__)


async def get_orders(session: AsyncSession, pagination: PaginationParam):
    try:
        stmt = select(Order).options(
            selectinload(Order.customer),
            selectinload(Order.location),
            selectinload(Order.payment_method),
        ).order_by(Order.created_at.desc())

        return await fetch_paginated_data(
            session=session,
            stmt=stmt,
            entity=Order,
            pagination=pagination,
            data_response_model=OrderDataResponse,
            order_by_field=Order.created_at,
            message="Orders fetched successfully"
        )
    except Exception as e:
        # Handle the exception (e.g., log it, return an error response, etc.)
        logging.error(f"Error fetching orders: {e}", exc_info=True)
        return Exception(f"Error fetching orders: {e}")
