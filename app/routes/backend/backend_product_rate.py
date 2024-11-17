from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import product_rate

product_rate_router = APIRouter(
    prefix="/product_rates",
    tags=["Backend Product Rate API"],
    responses={404: {"description": "Not found"}},
)


@product_rate_router.get("", status_code=200)
async def get_product_rates(session: AsyncSession = Depends(get_session),
                            pagination: PaginationParam = Depends(PaginationParam)):
    return await product_rate.get_product_rates(session, pagination)


@product_rate_router.get("/{product_rate_id}", status_code=200)
async def get_product_rate(product_rate_id: str, session: AsyncSession = Depends(get_session)):
    return await product_rate.get_product_rate(product_rate_id, session)


@product_rate_router.post("", status_code=200)
async def create_product_rate(req: product_rate.ProductRateRequest, session: AsyncSession = Depends(get_session)):
    return await product_rate.create_product_rate(req, session)


@product_rate_router.put("/{product_rate_id}", status_code=200)
async def update_product_rate(product_rate_id: str, req: product_rate.ProductRateRequest,
                              session: AsyncSession = Depends(get_session)):
    return await product_rate.update_product_rate(product_rate_id, req, session)


@product_rate_router.delete("/{product_rate_id}", status_code=200)
async def delete_product_rate(product_rate_id: str, session: AsyncSession = Depends(get_session)):
    return await product_rate.delete_product_rate(product_rate_id, session)
