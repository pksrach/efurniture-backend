from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import product

frontend_product_router = APIRouter(
    prefix="/products",
    tags=["Frontend Product API"]
)


@frontend_product_router.get("", status_code=200)
async def get_products(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await product.get_products(session, pagination)


@frontend_product_router.get("/{product_id}", status_code=200)
async def get_product(product_id, session: AsyncSession = Depends(get_session)):
    return await product.get_product(product_id, session)
