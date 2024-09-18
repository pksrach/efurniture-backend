import logging

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config.settings import get_settings
from app.models.brand import Brand
from app.models.category import Category
from app.models.color import Color
from app.models.product import Product
from app.models.product_price import ProductPrice
from app.responses.product import ProductListResponse, ProductDataResponse, ProductResponse
from app.schemas.product import ProductRequest

settings = get_settings()


async def get_products(session: AsyncSession) -> ProductListResponse:
    stmt = (
        select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).order_by(Product.created_at.desc())
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    return ProductListResponse.from_entities(list(products))


async def get_product(id: str, session: AsyncSession) -> ProductResponse:
    stmt = (
        select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).where(Product.id == id)
    )
    result = await session.execute(stmt)
    product = result.scalars().first()

    if product is None:
        return ProductResponse(
            data=None,
            message="Product not found"
        )

    return ProductResponse.from_entity(product)


async def create_product(req: ProductRequest, session: AsyncSession) -> ProductResponse:
    try:
        # Validate category_id
        stmt = select(Category).where(Category.id == req.category_id)
        result = await session.execute(stmt)
        category = result.scalar()
        if not category:
            return ProductResponse(
                data=None,
                message="Invalid category_id. Category does not exist."
            )

        # Validate brand_id
        stmt = select(Brand).where(Brand.id == req.brand_id)
        result = await session.execute(stmt)
        brand = result.scalar()
        if not brand:
            return ProductResponse(
                data=None,
                message="Invalid brand_id. Brand does not exist."
            )

        # Check if a product with the same name exists
        stmt = select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).where(Product.name == req.name)
        result = await session.execute(stmt)
        product = result.scalar()

        if product:
            return ProductResponse(
                data=ProductDataResponse.from_entity(product),
                message=f"Product already exists"
            )

        # Create the new product
        product = Product(
            name=req.name,
            description=req.description,
            attachment=req.attachment,
            category_id=req.category_id,
            brand_id=req.brand_id,
        )
        session.add(product)
        await session.flush()  # Flush to get product.id populated without committing

        # Validate product_prices not empty
        if not req.product_prices:
            logging.error("Product prices cannot be empty", exc_info=True)
            return ProductResponse(
                data=None,
                message="Product prices cannot be empty"
            )
        # Validate and add ProductPrice objects
        product_prices = []
        for product_price_request in req.product_prices:
            # Validate color_id
            stmt = select(Color).where(Color.id == product_price_request.color_id)
            result = await session.execute(stmt)
            color = result.scalar()

            if not color:
                return ProductResponse(
                    data=None,
                    message=f"Invalid color_id: {product_price_request.color_id}. Color does not exist."
                )

            # Check if a ProductPrice already exists for the same product and color
            stmt = select(ProductPrice).where(
                and_(
                    ProductPrice.product_id == product.id,
                    ProductPrice.color_id == product_price_request.color_id
                )
            )
            result = await session.execute(stmt)
            existing_product_price = result.scalar()

            if existing_product_price:
                color_name = existing_product_price.color.name if existing_product_price.color else "Unknown Color"
                return ProductResponse(
                    data=None,
                    message=f"Product price already exists with the same color {color_name} and product {product.name}"
                )

            # Add new ProductPrice to the list
            product_prices.append(ProductPrice(
                product_id=product.id,
                color_id=product_price_request.color_id,
                size=product_price_request.size,
                price=product_price_request.price
            ))

        session.add_all(product_prices)  # Add the validated product prices to the session
        await session.flush()  # Ensure the changes are flushed to the database

        # Refresh the product with relationships, including product_prices
        await session.refresh(product, attribute_names=["category", "brand", "product_prices"])
        for product_price in product.product_prices:
            await session.refresh(product_price, attribute_names=["color"])

        # Commit the transaction after all operations
        await session.commit()

        return ProductResponse(
            data=ProductDataResponse.from_entity(product),
            message="Product created successfully"
        )

    except Exception as e:
        await session.rollback()  # Ensure any transaction is rolled back in case of error
        raise e


async def update_product(id: str, req: ProductRequest, session: AsyncSession) -> ProductResponse:
    try:
        # Fetch the existing product
        stmt = select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).where(Product.id == id)
        result = await session.execute(stmt)
        product = result.scalar()

        if product is None:
            return ProductResponse(
                data=None,
                message="Product not found"
            )

        # Validate category_id
        stmt = select(Category).where(Category.id == req.category_id)
        result = await session.execute(stmt)
        category = result.scalar()
        if not category:
            return ProductResponse(
                data=None,
                message="Invalid category_id. Category does not exist."
            )

        # Validate brand_id
        stmt = select(Brand).where(Brand.id == req.brand_id)
        result = await session.execute(stmt)
        brand = result.scalar()
        if not brand:
            return ProductResponse(
                data=None,
                message="Invalid brand_id. Brand does not exist."
            )

        # Update product details
        product.name = req.name
        product.description = req.description
        product.attachment = req.attachment
        product.category_id = req.category_id
        product.brand_id = req.brand_id

        # Set of existing ProductPrice IDs to track which ones to delete
        existing_product_price_ids = {pp.id for pp in product.product_prices}

        # Validate product_prices not empty
        if not req.product_prices:
            logging.error(f"Product prices cannot be empty")
            return ProductResponse(
                data=None,
                message="Product prices cannot be empty"
            )
        # Process new ProductPrice entries
        new_product_prices = []
        for product_price_request in req.product_prices:
            # Validate color_id
            stmt = select(Color).where(Color.id == product_price_request.color_id)
            result = await session.execute(stmt)
            color = result.scalar()

            if not color:
                return ProductResponse(
                    data=None,
                    message=f"Invalid color_id: {product_price_request.color_id}. Color does not exist."
                )

            # Check if this ProductPrice entry exists
            stmt = select(ProductPrice).where(
                and_(
                    ProductPrice.product_id == product.id,
                    ProductPrice.color_id == product_price_request.color_id
                )
            )
            result = await session.execute(stmt)
            existing_product_price = result.scalar()

            if existing_product_price:
                # Update existing product price if it already exists
                existing_product_price.size = product_price_request.size
                existing_product_price.price = product_price_request.price
                existing_product_price_ids.discard(existing_product_price.id)  # Remove from set
            else:
                # Add new ProductPrice entry
                new_product_prices.append(ProductPrice(
                    product_id=product.id,
                    color_id=product_price_request.color_id,
                    size=product_price_request.size,
                    price=product_price_request.price
                ))

        # Delete product prices that are not in the updated list
        for product_price_id in existing_product_price_ids:
            stmt = select(ProductPrice).where(ProductPrice.id == product_price_id)
            result = await session.execute(stmt)
            product_price = result.scalar()
            if product_price:
                await session.delete(product_price)

        # Add new ProductPrice entries to the session
        session.add_all(new_product_prices)
        await session.flush()  # Ensure changes are flushed to the database

        # Refresh the product with relationships, including product_prices
        await session.refresh(product, attribute_names=["category", "brand", "product_prices"])
        for product_price in product.product_prices:
            await session.refresh(product_price, attribute_names=["color"])

        # Commit the transaction
        await session.commit()

        return ProductResponse(
            data=ProductDataResponse.from_entity(product),
            message="Product updated successfully"
        )

    except Exception as e:
        await session.rollback()  # Roll back the transaction in case of error
        logging.error(f"Error updating product: {e}", exc_info=True)
        return ProductResponse(
            data=None,
            message=str(e)
        )


async def delete_product(id: str, session: AsyncSession):
    stmt = select(Product).where(Product.id == id)
    result = await session.execute(stmt)
    product = result.scalar()

    if product is None:
        return ProductResponse(
            data=None,
            message="Product not found"
        )

    await session.delete(product)
    await session.commit()
    return {
        "message": "Product deleted successfully"
    }
