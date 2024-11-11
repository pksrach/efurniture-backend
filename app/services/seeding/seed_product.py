import random
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.models.product_price import ProductPrice
from app.models.category import Category
from app.models.brand import Brand
from app.models.color import Color
from app.schemas.product import ProductRequest, ProductPriceRequest
import uuid

class SeedProduct:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def product_exists(self, name: str) -> bool:
        stmt = select(Product).filter(Product.name == name)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def get_random_category_id(self) -> uuid.UUID:
        stmt = select(Category.id)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()
        return random.choice(categories) if categories else None

    async def get_random_brand_id(self) -> uuid.UUID:
        stmt = select(Brand.id)
        result = await self.session.execute(stmt)
        brands = result.scalars().all()
        return random.choice(brands) if brands else None

    async def get_random_color_id(self) -> uuid.UUID:
        stmt = select(Color.id)
        result = await self.session.execute(stmt)
        colors = result.scalars().all()
        return random.choice(colors) if colors else None

    async def get_random_image_url(self) -> str:
        image_urls = [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmYTF1-8uEPDjgrNDJjKOuViYeWcxvg8HDRg&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoKR5QdSXiTB_WVOgJ3vcAGkhUo1SlQXsO1Q&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7jiYA2kDNVpJvwf67ouZq2ex89VThhiMHpw&s",
            # Add more image URLs here
        ]
        return random.choice(image_urls)

    async def seed_product(self):
        products = [
            ProductRequest(
                name="Product 1",
                description="Description for product 1",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=10.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=12.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=14.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 2",
                description="Description for product 2",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=20.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=22.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=24.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 3",
                description="Description for product 3",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=30.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=32.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=34.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 4",
                description="Description for product 4",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=40.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=42.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=44.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 5",
                description="Description for product 5",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=50.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=52.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=54.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 6",
                description="Description for product 6",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=60.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=62.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=64.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 7",
                description="Description for product 7",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=70.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=72.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=74.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 8",
                description="Description for product 8",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=80.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=82.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=84.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 9",
                description="Description for product 9",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=90.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=92.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=94.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 10",
                description="Description for product 10",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=100.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=102.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=104.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 11",
                description="Description for product 11",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=110.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=112.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=114.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 12",
                description="Description for product 12",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=120.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=122.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=124.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 13",
                description="Description for product 13",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=130.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=132.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=134.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 14",
                description="Description for product 14",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=140.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=142.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=144.0, color_id=await self.get_random_color_id(), size="L")
                ]
            ),
            ProductRequest(
                name="Product 15",
                description="Description for product 15",
                attachment=await self.get_random_image_url(),
                category_id=await self.get_random_category_id(),
                brand_id=await self.get_random_brand_id(),
                product_prices=[
                    ProductPriceRequest(price=150.0, color_id=await self.get_random_color_id(), size="S"),
                    ProductPriceRequest(price=152.0, color_id=await self.get_random_color_id(), size="M"),
                    ProductPriceRequest(price=154.0, color_id=await self.get_random_color_id(), size="L")
                ]
            )
        ]

        for product in products:
            if not await self.product_exists(product.name):
                new_product = Product(
                    name=product.name,
                    description=product.description,
                    attachment=product.attachment,
                    category_id=product.category_id,
                    brand_id=product.brand_id,
                    is_active=True
                )
                self.session.add(new_product)
                await self.session.flush()  # Ensure the product ID is available

                for price in product.product_prices:
                    new_product_price = ProductPrice(
                        price=price.price,
                        color_id=price.color_id,
                        size=price.size,
                        product_id=new_product.id
                    )
                    self.session.add(new_product_price)

    async def run(self):
        async with self.session.begin():
            await self.seed_product()
        await self.session.commit()

        return "Products seeded successfully"