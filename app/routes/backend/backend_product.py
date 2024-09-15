from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.schemas.product import ProductRequest
from app.services import product
from app.services.product import create_product

product_router = APIRouter(
    prefix="/products",
    tags=["Backend Product API"],
    responses={404: {"description": "Not found"}},
)


@product_router.get("", status_code=200)
async def get_products(session: AsyncSession = Depends(get_session)):
    return await product.get_products(session)


@product_router.get("/{id}", status_code=200)
async def get_product(id: str, session: AsyncSession = Depends(get_session)):
    return await product.get_product(id, session)


@product_router.post("", status_code=201)
async def create_product_endpoint(req: ProductRequest, session: AsyncSession = Depends(get_session)):
    return await create_product(req, session)

#
# @color_router.put("/{id}", status_code=200)
# async def update_color(id: str, req: product.ColorRequest, session: AsyncSession = Depends(get_session)):
#     return await product.update_color(id, req, session)
#
#
# @color_router.delete("/{id}", status_code=200)
# async def delete_color(id: str, session: AsyncSession = Depends(get_session)):
#     return await product.delete_color(id, session)