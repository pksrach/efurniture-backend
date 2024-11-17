import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.cart import Cart
from app.models.product import Product
from app.models.product_price import ProductPrice
from app.models.user import User
from app.responses.frontend.frontend_cart_response import FrontendCartResponse, FrontendCartDataResponse, \
    FrontendCartListResponse
from app.schemas.cart import CartRequest

logger = logging.getLogger(__name__)


async def get_carts(user, session: AsyncSession):
    logger.info("Getting carts...")
    try:
        stmt = (
            select(Cart).options(
                selectinload(Cart.product_price).selectinload(ProductPrice.product).selectinload(Product.brand),
                selectinload(Cart.product_price).selectinload(ProductPrice.product).selectinload(Product.category),
                selectinload(Cart.product_price).selectinload(ProductPrice.color),
                selectinload(Cart.user)
            ).join(Cart.user).where(User.id == user.id)
        )

        result = await session.execute(stmt)
        carts = list(result.scalars().all())

        if not carts:
            logger.info("No carts found")
            return FrontendCartResponse(
                data=None,
                message="No carts found"
            )

        return FrontendCartListResponse.from_entity(carts)

    except SQLAlchemyError as e:
        logger.error(f"Error fetching carts: {e}")
        return FrontendCartResponse(
            data=None,
            message="Error fetching carts"
        )


async def add_cart(req: CartRequest, user, session: AsyncSession):
    logger.info("Adding cart...")
    try:
        # Check qty first if is null or less than 1 then raise error
        if not req.qty or req.qty < 1:
            logger.error("Quantity must be greater than 0")
            return FrontendCartResponse(
                data=None,
                message="Quantity must be greater than 0"
            )

        # Check if product_price_id exists
        stmt = (select(ProductPrice).options(
            selectinload(ProductPrice.product),
            selectinload(ProductPrice.product).selectinload(Product.brand),
            selectinload(ProductPrice.product).selectinload(Product.category),
            selectinload(ProductPrice.color)
        ).where(ProductPrice.id == req.product_price_id))
        result = await session.execute(stmt)
        product_price = result.scalar()

        if product_price is None:
            logger.error("Product price not found")
            return FrontendCartResponse(
                data=None,
                message="Product price not found"
            )

        product = product_price.product

        # Check if product exists or not
        if product is None:
            logger.error("Product not found")
            return FrontendCartResponse(
                data=None,
                message="Product not found"
            )

        # Check if cart item already exists for the user and product price
        stmt = (select(Cart).where(
            Cart.user_id == user.id,
            Cart.product_price_id == req.product_price_id
        ))
        result = await session.execute(stmt)
        existing_cart = result.scalar()

        if existing_cart:
            # Update the quantity of the existing cart item
            existing_cart.qty += req.qty
            existing_cart.updated_by = user.id
            session.add(existing_cart)
            await session.commit()
            await session.refresh(existing_cart, ['product_price'])

            logger.info("Cart updated successfully")
            return FrontendCartResponse(
                data=FrontendCartDataResponse.from_entity(existing_cart),
                message="Cart updated successfully"
            )
        else:
            # Create a new cart item
            new_cart = Cart(
                user_id=user.id,
                product_price_id=req.product_price_id,
                qty=req.qty
            )
            new_cart.created_by = user.id

            session.add(new_cart)
            await session.commit()
            await session.refresh(new_cart, ['product_price'])

            logger.info("Cart added successfully")
            return FrontendCartResponse(
                data=FrontendCartDataResponse.from_entity(new_cart),
                message="Cart added successfully"
            )

    except SQLAlchemyError as e:
        logger.error(f"Error adding cart: {e}")
        await session.rollback()
        return FrontendCartResponse(
            data=None,
            message="Error adding cart"
        )
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)


async def remove_cart(cart_id, user, session: AsyncSession):
    logger.info("Removing cart...")
    try:
        stmt = (select(Cart).where(
            Cart.id == cart_id,
            Cart.user_id == user.id
        ))
        result = await session.execute(stmt)
        cart = result.scalar()

        if cart is None:
            logger.error("Cart not found")
            return FrontendCartResponse(
                data=None,
                message="Cart not found"
            )

        await session.delete(cart)
        await session.commit()

        logger.info("Cart removed successfully")
        return FrontendCartResponse(
            data=None,
            message="Cart removed successfully"
        )

    except SQLAlchemyError as e:
        logger.error(f"Error removing cart: {e}")
        await session.rollback()
        return FrontendCartResponse(
            data=None,
            message="Error removing cart"
        )
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)


async def remove_all_carts(user, session: AsyncSession):
    logger.info("Removing all carts...")
    try:
        stmt = (select(Cart).where(Cart.user_id == user.id))
        result = await session.execute(stmt)
        carts = result.scalars().all()

        if not carts:
            logger.info("No carts found")
            return FrontendCartResponse(
                data=None,
                message="No carts found"
            )

        for cart in carts:
            await session.delete(cart)

        await session.commit()

        logger.info("All carts removed successfully")
        return FrontendCartResponse(
            data=None,
            message="All carts removed successfully"
        )

    except SQLAlchemyError as e:
        logger.error(f"Error removing all carts: {e}")
        await session.rollback()
        return FrontendCartResponse(
            data=None,
            message="Error removing all carts"
        )
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)


async def add_all_carts(req: list[CartRequest], user, session: AsyncSession):
    logger.info("Adding carts...")
    try:
        # Check if cart items already exist for the user
        stmt = (select(Cart).where(Cart.user_id == user.id))
        result = await session.execute(stmt)
        existing_carts = result.scalars().all()

        # Create a dictionary of existing cart items for easy access
        existing_cart_dict = {cart.product_price_id: cart for cart in existing_carts}

        new_carts = []
        for cart_req in req:
            # Check qty first if is null or less than 1 then raise error
            if not cart_req.qty or cart_req.qty < 1:
                logger.error("Quantity must be greater than 0")
                return FrontendCartResponse(
                    data=None,
                    message="Quantity must be greater than 0"
                )

            # Check if product_price_id exists
            stmt = (select(ProductPrice).options(
                selectinload(ProductPrice.product),
                selectinload(ProductPrice.product).selectinload(Product.brand),
                selectinload(ProductPrice.product).selectinload(Product.category),
                selectinload(ProductPrice.color)
            ).where(ProductPrice.id == cart_req.product_price_id))
            result = await session.execute(stmt)
            product_price = result.scalar()

            if product_price is None:
                logger.error("Product price not found")
                return FrontendCartResponse(
                    data=None,
                    message="Product price not found"
                )

            product = product_price.product

            # Check if product exists or not
            if product is None:
                logger.error("Product not found")
                return FrontendCartResponse(
                    data=None,
                    message="Product not found"
                )

            # Check if cart item already exists for the user and product price
            stmt = (select(Cart).where(
                Cart.user_id == user.id,
                Cart.product_price_id == cart_req.product_price_id
            ))
            result = await session.execute(stmt)
            existing_cart = result.scalar()

            if existing_cart:
                # Update the quantity of the existing cart item
                existing_cart.qty += cart_req.qty
                existing_cart.updated_by = user.id
                session.add(existing_cart)
                await session.refresh(existing_cart, ['product_price'])

                logger.info("Cart updated successfully")
                new_carts.append(existing_cart)
            else:
                # Create a new cart item
                new_cart = Cart(
                    user_id=user.id,
                    product_price_id=cart_req.product_price_id,
                    qty=cart_req.qty
                )
                new_cart.created_by = user.id

                session.add(new_cart)
                await session.commit()
                await session.refresh(new_cart, ['product_price'])

                logger.info("Cart added successfully")
                new_carts.append(new_cart)

        await session.commit()
        return FrontendCartListResponse.from_entity(new_carts)

    except SQLAlchemyError as e:
        logger.error(f"Error adding carts: {e}")
        await session.rollback()
        return FrontendCartResponse(
            data=None,
            message="Error adding carts"
        )
    except ValueError as e:
        logger.error(e)
        raise ValueError(e)
