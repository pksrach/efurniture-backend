import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customer
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.schemas.order import OrderRequest

logger = logging.getLogger(__name__)


async def create_order(req: OrderRequest, user, session: AsyncSession):
    print("Creating order...")
    try:
        # Fetch customer id from user
        print("user_id: ", user.id)
        stmt = (
            select(Customer)
            .where(Customer.user_id == user.id)
        )
        result = await session.execute(stmt)
        customer = result.scalar()

        if customer is None:
            raise ValueError("Customer not found")
        print("customer_id ", customer.id)
        customer_id = customer.id

        # Create the order
        new_order = Order(
            order_date=req.order_date,
            order_status='pending',
            total=0,
            discount=0,
            amount=0,
            customer_id=customer_id,
            location_id=req.location_id,
            location_price=0,
            payment_method_id=req.payment_method_id,
            payment_attachment=req.payment_attachment,
            note=req.note,
            created_by=user.id
        )
        session.add(new_order)
        await session.flush()  # Ensure new_order.id is available

        print("new_order.id: ", new_order.id)

        # Create order details
        for detail in req.details:
            new_order_detail = OrderDetail(
                order_id=new_order.id,
                product_id=detail.product_id,
                product_price_id=detail.product_price_id,
                category_id=detail.category_id,
                brand_id=detail.brand_id,
                color_id=detail.color_id,
                size=detail.size,
                price=detail.price,
                qty=detail.qty,
                total=detail.price * detail.qty,
                created_by=user.id
            )
            # Calculate amount
            new_order.amount += new_order_detail.total

            session.add(new_order_detail)

        print("new_order.amount: ", new_order.amount)

        await session.commit()
        await session.refresh(new_order)

        logger.info("Order created successfully")
        return new_order

    except SQLAlchemyError as e:
        logger.error(f"Error creating order: {e}")
        await session.rollback()
        return {"message": "Error creating order"}
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)
