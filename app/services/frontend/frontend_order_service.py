import logging
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.schemas.order import OrderRequest
from app.services.frontend import frontend_cart_service
from app.services.location import get_location
from app.services.order_history import create_order_history

logger = logging.getLogger(__name__)


async def create_order(req: OrderRequest, user, session: AsyncSession):
    print("Creating order...")
    try:
        # Fetch customer id from user
        stmt = (
            select(Customer)
            .where(Customer.user_id == user.id)
        )
        result = await session.execute(stmt)
        customer = result.scalar()

        if customer is None:
            raise ValueError("Customer not found")
        customer_id = customer.id

        # Assign location price
        location = await get_location(req.location_id, session)
        if location.data is None:
            raise ValueError("Location not found")

        # Create the order
        new_order = Order(
            order_date=datetime.now(),
            order_status='pending',
            amount=0,
            customer_id=customer_id,
            location_id=location.data.id,
            location_price=location.data.price,
            payment_method_id=req.payment_method_id,
            payment_attachment=req.payment_attachment,
            note=req.note,
            created_by=user.id
        )
        session.add(new_order)

        await session.flush()  # Ensure new_order.id is available

        # Create order details
        for detail in req.details:
            new_order_detail = OrderDetail(
                order_id=new_order.id,
                product_id=detail.product_id,
                category_id=detail.category_id,
                brand_id=detail.brand_id,
                color_id=detail.color_id,
                size=detail.size,
                price=detail.price,
                qty=detail.qty,
                total=detail.price * detail.qty,
                created_by=user.id
            )
            # Calculate order amount
            new_order.amount += new_order_detail.total
            session.add(new_order_detail)

        # Add order history
        await create_order_history(user.id, new_order.id, new_order.order_status, session)

        await session.commit()
        await session.refresh(new_order)

        # Clear cart
        await frontend_cart_service.remove_all_carts(user, session)

        logger.info("Order created successfully")
        return new_order

    except SQLAlchemyError as e:
        logger.error(f"Error creating order: {e}")
        await session.rollback()
        return {"message": "Error creating order", "error": str(e)}
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)
