from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.settings import get_settings
from app.models.product import Product
from app.responses.product import ProductListResponse, ProductDataResponse, KeyValueResponse, ProductResponse
from app.schemas.product import ProductRequest

settings = get_settings()


async def get_products(session: AsyncSession) -> ProductListResponse:
    stmt = (
        select(Product)
        .options(
            joinedload(Product.category), joinedload(Product.brand)
        ).order_by(Product.created_at.desc())
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    return ProductListResponse.from_entities(list(products))


async def get_product(id: str, session: AsyncSession) -> ProductResponse:
    stmt = (
        select(Product)
        .options(
            joinedload(Product.category), joinedload(Product.brand)
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
        # Check exists name or not
        stmt = select(Product).where(Product.name == req.name)
        result = await session.execute(stmt)
        product = result.scalars().first()
        if product:
            return ProductResponse(
                data=ProductDataResponse(
                    id=product.id,
                    name=product.name,
                    description=product.description,
                    attachment=product.attachment,
                    category=KeyValueResponse(
                        key=product.category.id if product.category else None,
                        value=product.category.name if product.category else None,
                    ),
                    brand=KeyValueResponse(
                        key=product.brand.id if product.brand else None,
                        value=product.brand.name if product.brand else None,
                    ),
                    is_active=product.is_active
                ),
                message="Product already exists"
            )

        product = Product(
            name=req.name,
            description=req.description,
            attachment=req.attachment,
            category_id=req.category_id,
            brand_id=req.brand_id,
        )
        session.add(product)
        await session.commit()

        return ProductResponse.from_entity(product)
    except Exception as e:
        return ProductResponse(
            data=None,
            message=str(e)
        )

#
# async def update_color(id: str, req: ColorRequest, session: AsyncSession) -> ProductResponse:
#     stmt = select(Product).where(Product.id == id)
#     result = await session.execute(stmt)
#     product = result.scalars().first()
#
#     if product is None:
#         return ProductResponse(
#             data=None,
#             message="Product not found"
#         )
#
#     product.code = req.code
#     product.name = req.name
#     product.highlight = req.highlight
#     await session.commit()
#     return ProductResponse(
#         data=ProductDataResponse(
#             id=product.id,
#             code=product.code,
#             name=product.name,
#             highlight=product.highlight,
#         ),
#         message="Product updated successfully"
#     )
#
#
# async def delete_color(id: str, session: AsyncSession) -> ProductResponse:
#     stmt = select(Product).where(Product.id == id)
#     result = await session.execute(stmt)
#     product = result.scalars().first()
#
#     if product is None:
#         return ProductResponse(
#             data=None,
#             message="Product not found"
#         )
#
#     await session.delete(product)
#     await session.commit()
#     return ProductResponse(
#         data=ProductDataResponse(
#             id=product.id,
#             code=product.code,
#             name=product.name,
#             highlight=product.highlight,
#         ),
#         message="Product deleted successfully"
#     )
