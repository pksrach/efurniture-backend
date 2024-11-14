import logging

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.security import get_backend_user
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.order_history import OrderHistory
from app.models.staff import Staff
from app.models.user import User
from app.responses.order import OrderDataResponse, OrderResponse
from app.responses.order_detail import OrderDetailResponse, OrderDetailListResponse, OrderDetailDataResponse
from app.responses.order_history import OrderListHistoryResponse
from app.responses.paginated_response import PaginationParam
from app.services.base_service import fetch_paginated_data
from app.services.order_history import create_order_history

logger = logging.getLogger(__name__)


async def get_orders(session: AsyncSession, pagination: PaginationParam):
    try:
        stmt = select(Order).options(
            selectinload(Order.customer),
            selectinload(Order.location),
            selectinload(Order.payment_method),
            selectinload(Order.staff)
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
        logger.error(f"Error fetching orders: {e}", exc_info=True)
        return {
            "message": "An error occurred while fetching orders.",
            "error": str(e)
        }


async def get_order(order_id, session: AsyncSession):
    try:
        stmt = select(Order).options(
            selectinload(Order.customer),
            selectinload(Order.location),
            selectinload(Order.payment_method),
            selectinload(Order.staff)
        ).where(Order.id == order_id)

        result = await session.execute(stmt)
        order = result.scalars().first()

        if not order:
            return OrderResponse(
                data=None,
                message="Order not found!"
            )

        return OrderResponse(
            data=OrderDataResponse.from_entity(order),
            message="Order fetched successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching order: {e}", exc_info=True)
        return {
            "message": "An error occurred while fetching order.",
            "error": str(e)
        }


async def get_order_details(order_id, session: AsyncSession):
    try:
        stmt = select(OrderDetail).options(
            selectinload(OrderDetail.product),
            selectinload(OrderDetail.category),
            selectinload(OrderDetail.brand),
            selectinload(OrderDetail.color),
        ).where(OrderDetail.order_id == order_id)

        result = await session.execute(stmt)
        order_details = result.scalars().all()

        if not order_details:
            return OrderDetailResponse(
                data=None,
                message="Order details not found!"
            )

        return OrderDetailListResponse(
            data=[OrderDetailDataResponse.from_entity(order_detail) for order_detail in order_details],
            message="Order details fetched successfully"
        )
    except Exception as e:
        logger.error(f"Error fetching order: {e}", exc_info=True)
        return {
            "message": "An error occurred while fetching order.",
            "error": str(e)
        }


async def process_order(
        order_id: str,
        order_status,
        session: AsyncSession,
        current_user: User = Depends(get_backend_user)
):
    try:
        # Fetch the order
        stmt = select(Order).where(Order.id == order_id)
        result = await session.execute(stmt)
        order = result.scalars().first()

        if not order:
            return OrderResponse(
                data=None,
                message="Order not found!"
            )

        # Check order status must be existed
        if order_status is None or order_status == "":
            return {
                "message": "Order status must be provided.",
                "error": "Invalid order status"
            }

        # Check if order status is same value update need to block
        if order_status.lower() == order.order_status.lower():
            return {
                "data": order.id,
                "message": f"Order status already {order_status.capitalize()}"
            }

        # Define valid status transitions
        valid_status_transitions = {
            "pending": ["accepted", "delivered", "done", "canceled"],
            "accepted": ["delivered", "done", "canceled"],
            "delivered": ["done", "canceled"],
            "done": ["canceled"],
            "canceled": []
        }

        # Check if the new status is a valid transition from the current status
        current_status = order.order_status.lower()
        if order_status.lower() not in valid_status_transitions[current_status]:
            return {
                "data": order.id,
                "message": f"Invalid status transition from {current_status.capitalize()} to {order_status.capitalize()}"
            }

        # Update the order status to the new status
        order.order_status = order_status

        # Update the order status to accept
        order.order_status = order_status

        # Assign staff modifying the order
        staff_stmt = select(Staff).where(Staff.user_id == current_user.id)
        staff_result = await session.execute(staff_stmt)
        # If exists, assign the staff to the order else assign None
        staff = staff_result.scalars().first()
        if staff:
            order.staff_id = staff.id
            order.updated_by = current_user.id

        # Create order history
        await create_order_history(current_user.id, order_id, order_status, session)

        await session.commit()

        return {
            "data": order.id,
            "message": f"Order has been {order_status}"
        }
    except Exception as e:
        logger.error(f"Error accepting order: {e}", exc_info=True)
        await session.rollback()
        return {
            "message": "An error occurred while accepting the order.",
            "error": str(e)
        }


async def get_order_histories(order_id: str, session: AsyncSession):
    try:
        stmt = select(OrderHistory).options(
            selectinload(OrderHistory.order)
        ).where(OrderHistory.order_id == order_id).order_by(OrderHistory.created_at.asc())

        result = await session.execute(stmt)
        order_histories = list(result.scalars().all())

        if not order_histories:
            return OrderListHistoryResponse(
                data=[],
                message="No order histories found!"
            )

        return OrderListHistoryResponse.from_entities(order_histories)
    except Exception as e:
        logger.error(f"Error fetching order histories: {e}", exc_info=True)
        return {
            "message": "An error occurred while fetching order histories.",
            "error": str(e)
        }
