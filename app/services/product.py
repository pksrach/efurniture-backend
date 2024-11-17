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
from app.responses.paginated_response import PaginationParam
from app.responses.product import ProductDataResponse, ProductResponse
from app.schemas.product import ProductRequest
from app.services.base_service import fetch_paginated_data

settings = get_settings()


async def get_products(session: AsyncSession, pagination: PaginationParam):
    stmt = (
        select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).order_by(Product.created_at.desc())
    )

    return await fetch_paginated_data(
        session=session,
        stmt=stmt,
        entity=Product,
        pagination=pagination,
        data_response_model=ProductDataResponse,
        order_by_field=Product.created_at,
        message="Products fetched successfully"
    )


async def get_product(product_id: str, session: AsyncSession) -> ProductResponse:
    stmt = (
        select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)  # Load the color for product prices
        ).where(Product.id == product_id)
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
        await validate_category(req.category_id, session)
        await validate_brand(req.brand_id, session)

        if await validate_product_name(req.name, session):
            return ProductResponse(
                data=None,
                message="Product already exists"
            )

        product = Product(
            name=req.name,
            description=req.description,
            attachment=req.attachment,
            category_id=req.category_id,
            brand_id=req.brand_id
        )
        session.add(product)
        await session.flush()

        product_prices = await validate_and_add_product_prices(req.product_prices, product.id, session)
        session.add_all(product_prices)
        await session.flush()

        await session.refresh(product, attribute_names=["category", "brand", "product_prices"])
        for product_price in product.product_prices:
            await session.refresh(product_price, attribute_names=["color"])

        await session.commit()

        return ProductResponse(
            data=ProductDataResponse.from_entity(product),
            message="Product created successfully"
        )
    except ValueError as e:
        await session.rollback()
        return ProductResponse(
            data=None,
            message=str(e)
        )
    except Exception as e:
        await session.rollback()
        raise e


async def update_product(product_id: str, req: ProductRequest, session: AsyncSession) -> ProductResponse:
    try:
        stmt = select(Product).options(
            selectinload(Product.category),
            selectinload(Product.brand),
            selectinload(Product.product_prices).selectinload(ProductPrice.color)
        ).where(Product.id == product_id)
        result = await session.execute(stmt)
        product = result.scalar()

        if product is None:
            return ProductResponse(
                data=None,
                message="Product not found"
            )

        await validate_category(req.category_id, session)
        await validate_brand(req.brand_id, session)

        product.name = req.name
        product.description = req.description
        product.attachment = req.attachment
        product.category_id = req.category_id
        product.brand_id = req.brand_id

        # Collect existing ProductPrice IDs
        existing_product_price_ids = {pp.id for pp in product.product_prices}

        # Validate and process new and updated ProductPrice entries
        new_product_prices = await validate_and_add_product_prices(
            req.product_prices,
            product.id,
            session,
            existing_product_price_ids
        )

        # Handle updates to existing ProductPrice entries
        for product_price_request in req.product_prices:
            stmt = select(ProductPrice).where(
                and_(
                    ProductPrice.product_id == product.id,
                    ProductPrice.color_id == product_price_request.color_id
                )
            )
            result = await session.execute(stmt)
            existing_product_price = result.scalar()

            if existing_product_price:
                if existing_product_price.id in existing_product_price_ids:
                    # Update existing ProductPrice
                    existing_product_price.size = product_price_request.size
                    existing_product_price.price = product_price_request.price
                    existing_product_price_ids.remove(existing_product_price.id)
            else:
                # If not found, it should be a new ProductPrice entry
                new_product_prices.append(ProductPrice(
                    product_id=product.id,
                    color_id=product_price_request.color_id,
                    size=product_price_request.size,
                    price=product_price_request.price
                ))

        # Delete product prices that are no longer valid
        for product_price_id in existing_product_price_ids:
            stmt = select(ProductPrice).where(ProductPrice.id == product_price_id)
            result = await session.execute(stmt)
            product_price = result.scalar()
            if product_price:
                await session.delete(product_price)

        # Add new ProductPrice entries
        session.add_all(new_product_prices)
        await session.flush()

        # Refresh the product with relationships, including product_prices
        await session.refresh(product, attribute_names=["category", "brand", "product_prices"])
        for product_price in product.product_prices:
            await session.refresh(product_price, attribute_names=["color"])

        await session.commit()

        return ProductResponse(
            data=ProductDataResponse.from_entity(product),
            message="Product updated successfully"
        )
    except ValueError as e:
        await session.rollback()
        return ProductResponse(
            data=None,
            message=str(e)
        )
    except Exception as e:
        await session.rollback()
        logging.error(f"Error updating product: {e}", exc_info=True)
        return ProductResponse(
            data=None,
            message=str(e)
        )


async def delete_product(product_id: str, session: AsyncSession):
    stmt = select(Product).where(Product.id == product_id)
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


async def validate_category(category_id: str, session: AsyncSession) -> Category:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar()
    if not category:
        raise ValueError("Invalid category_id. Category does not exist.")
    return category


async def validate_brand(brand_id: str, session: AsyncSession) -> Brand:
    stmt = select(Brand).where(Brand.id == brand_id)
    result = await session.execute(stmt)
    brand = result.scalar()
    if not brand:
        raise ValueError("Invalid brand_id. Brand does not exist.")
    return brand


async def validate_color(color_id: str, session: AsyncSession) -> Color:
    stmt = select(Color).where(Color.id == color_id)
    result = await session.execute(stmt)
    color = result.scalar()
    if not color:
        raise ValueError(f"Invalid color_id: {color_id}. Color does not exist.")
    return color


async def validate_product_name(name: str, session: AsyncSession) -> Product:
    stmt = select(Product).options(
        selectinload(Product.category),
        selectinload(Product.brand),
        selectinload(Product.product_prices).selectinload(ProductPrice.color)
    ).where(Product.name == name)
    result = await session.execute(stmt)
    return result.scalar()


async def validate_and_add_product_prices(
        req_prices,
        product_id,
        session: AsyncSession,
        existing_product_prices_ids=None
):
    product_prices = []
    if existing_product_prices_ids is None:
        existing_product_prices_ids = set()

    # validate product must not empty
    if not req_prices:
        raise ValueError("Product prices cannot be empty.")

    for product_price_request in req_prices:
        color = await validate_color(product_price_request.color_id, session)

        # Check if the ProductPrice entry already exists
        stmt = select(ProductPrice).where(
            and_(
                ProductPrice.product_id == product_id,
                ProductPrice.color_id == product_price_request.color_id
            )
        )
        result = await session.execute(stmt)
        existing_product_price = result.scalar()

        if existing_product_price:
            if existing_product_price.id not in existing_product_prices_ids:
                # If it exists but is not in the list of IDs to update, raise an error
                raise ValueError(f"Product price already exists with the same color {color.name} and product.")
            # If it exists and is part of the IDs to update, no need to add to new entries
            continue

        # Add new ProductPrice to the list
        product_prices.append(ProductPrice(
            product_id=product_id,
            color_id=product_price_request.color_id,
            size=product_price_request.size,
            price=product_price_request.price
        ))

    if not product_prices and not existing_product_prices_ids:
        raise ValueError("Product prices cannot be empty.")

    return product_prices
