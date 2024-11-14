from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.schemas.product import ProductRequest
from app.services import product

product_router = APIRouter(
    prefix="/products",
    tags=["Backend Product API"],
    responses={404: {"description": "Not found"}},
)


@product_router.get("", status_code=200)
async def get_products(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await product.get_products(session, pagination)


@product_router.get("/{product_id}", status_code=200)
async def get_product(product_id: str, session: AsyncSession = Depends(get_session)):
    return await product.get_product(product_id, session)


@product_router.post("", status_code=201)
async def create_product(req: ProductRequest, session: AsyncSession = Depends(get_session)):
    return await product.create_product(req, session)


@product_router.put("/{product_id}", status_code=200)
async def update_color(product_id: str, req: ProductRequest, session: AsyncSession = Depends(get_session)):
    return await product.update_product(product_id, req, session)


@product_router.delete("/{product_id}", status_code=200)
async def delete_color(product_id: str, session: AsyncSession = Depends(get_session)):
    return await product.delete_product(product_id, session)
