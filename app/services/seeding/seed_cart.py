import random

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.models.product_price import ProductPrice
from app.schemas.cart import CartRequest


class SeedCart:
    def __init__(self, user, session: AsyncSession):
        self.user = user
        self.session = session

    async def get_random_product(self) -> Product:
        stmt = select(Product).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_price(self, product: Product) -> ProductPrice:
        stmt = select(ProductPrice).filter(ProductPrice.product_id == product.id).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def seed_random_carts(self, add_all_carts):
        cart_requests = []
        for _ in range(random.randrange(3, 7)):  # Randomly add 3 to 6 items
            product = await self.get_random_product()
            product_price = await self.get_product_price(product)
            qty = random.randrange(1, 5)  # Random quantity between 1 and 5
            cart_requests.append(CartRequest(product_price_id=product_price.id, qty=qty))

        await add_all_carts(cart_requests, self.user, self.session)

    async def run(self, add_all_carts):
        await self.seed_random_carts(add_all_carts)
        return "Seeding cart completed successfully."
