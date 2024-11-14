from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order_history import OrderHistory


async def create_order_history(user_id, order_id, order_status, session: AsyncSession):
    new_order_history = OrderHistory(
        order_id=order_id,
        order_status=order_status,
        created_by=user_id
    )
    session.add(new_order_history)
    await session.flush()
    return new_order_history
