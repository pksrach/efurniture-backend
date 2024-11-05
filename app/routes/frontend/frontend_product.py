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
async def products(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await product.get_products(session, pagination)
