from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import brand

brand_router = APIRouter(
    prefix="/brands",
    tags=["Backend Brand API"],
    responses={404: {"description": "Not found"}},
)


@brand_router.get("", status_code=200)
async def get_brands(session: AsyncSession = Depends(get_session),
                     pagination: PaginationParam = Depends(PaginationParam)):
    return await brand.get_brands(session, pagination)


@brand_router.get("/{brand_id}", status_code=200)
async def get_brand(brand_id: str, session: AsyncSession = Depends(get_session)):
    return await brand.get_brand(brand_id, session)


@brand_router.post("", status_code=201)
async def create_brand(req: brand.BrandRequest, session: AsyncSession = Depends(get_session)):
    return await brand.create_brand(req, session)


@brand_router.put("/{brand_id}", status_code=200)
async def update_brand(brand_id: str, req: brand.BrandRequest, session: AsyncSession = Depends(get_session)):
    return await brand.update_brand(brand_id, req, session)


@brand_router.delete("/{brand_id}", status_code=200)
async def delete_brand(brand_id: str, session: AsyncSession = Depends(get_session)):
    return await brand.delete_brand(brand_id, session)
