from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location
from app.models.payment_method import PaymentMethod
from app.schemas.order import OrderRequest, OrderDetailRequest
from app.services.frontend.frontend_cart_service import get_carts
from app.services.frontend.frontend_order_service import create_order


class SeedOrder:
    def __init__(self, user, session: AsyncSession):
        self.user = user
        self.session = session

    async def seed_order_from_carts(self):
        try:
            # Fetch cart data
            cart_response = await get_carts(self.user, self.session)
            if not cart_response.data:
                raise ValueError("No carts found")

            print("cart_response.data: ", cart_response.data)

            # Create order details from cart data
            order_details = []
            for cart in cart_response.data:
                order_details.append(OrderDetailRequest(
                    product_id=cart.product_id,
                    category_id=cart.category.key,
                    brand_id=cart.brand.key,
                    color_id=cart.color.key,
                    size=cart.size,
                    price=cart.price,
                    qty=cart.qty
                ))

            # Fetch a random payment method
            payment_method = await self.get_payment_method()

            location = await self.get_location()

            # Create order request
            order_request = OrderRequest(
                location_id=location.id,
                payment_method_id=payment_method.id,
                payment_attachment=payment_method.attachment_qr,
                note="Seed order",
                details=order_details
            )

            # Create order
            return await create_order(order_request, self.user, self.session)

        except ValueError as e:
            return {
                "message": "An error occurred while seeding order",
                "error": str(e)}

    async def get_location(self):
        stmt = select(Location).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_payment_method(self):
        stmt = select(PaymentMethod).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()
