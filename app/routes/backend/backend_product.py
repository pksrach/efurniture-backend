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


@product_router.get("/{id}", status_code=200)
async def get_product(id: str, session: AsyncSession = Depends(get_session)):
    return await product.get_product(id, session)


@product_router.post("", status_code=201)
async def create_product(req: ProductRequest, session: AsyncSession = Depends(get_session)):
    return await product.create_product(req, session)


@product_router.put("/{id}", status_code=200)
async def update_color(id: str, req: ProductRequest, session: AsyncSession = Depends(get_session)):
    return await product.update_product(id, req, session)


@product_router.delete("/{id}", status_code=200)
async def delete_color(id: str, session: AsyncSession = Depends(get_session)):
    return await product.delete_product(id, session)
