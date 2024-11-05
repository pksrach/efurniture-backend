import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.product_price import ProductPrice
from app.models.user import User

logger = logging.getLogger(__name__)


async def get_carts(user, session: AsyncSession):
    logger.info("Getting carts...")
    try:
        stmt = (
            select(Cart).options(
                selectinload(Cart.product_price).selectinload(ProductPrice.product),
                selectinload(Cart.product_price).selectinload(ProductPrice.color),
                selectinload(Cart.user)
            ).where(User.id == user.id)
        )

        result = await session.execute(stmt)
        carts = result.scalars().all()

        if not carts:
            logger.info("No carts found")
            return []

        return carts

    except SQLAlchemyError as e:
        logger.error(f"Error fetching carts: {e}")
        return []
