from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.services import product_rate

product_rate_router = APIRouter(
    prefix="/product_rates",
    tags=["Backend Product Rate API"],
    responses={404: {"description": "Not found"}},
)

@product_rate_router.get("",status_code=200)
async def get_product_rates(session: AsyncSession = Depends(get_session)):
    return await product_rate.get_product_rates(session)

@product_rate_router.post("/list-paginated",status_code=200)
async def get_paginated_product_rates(page: int = 1, limit: int = 10,session: AsyncSession = Depends(get_session)):
    return await product_rate.get_paginated_product_rates(session,page,limit)

@product_rate_router.get("/{id}", status_code=200)
async def get_product_rate(id:str, session: AsyncSession = Depends(get_session)):
    return await product_rate.get_product_rate(id,session)

@product_rate_router.post("", status_code=200)
async def create_product_rate(req: product_rate.ProductRateRequest, session: AsyncSession = Depends(get_session)):
    return await product_rate.create_product_rate(req,session)

@product_rate_router.put("/{id}", status_code=200)
async def update_product_rate(id:str,req: product_rate.ProductRateRequest,session: AsyncSession = Depends(get_session)):
    return await product_rate.update_product_rate(id,req,session)

@product_rate_router.delete("/{id}", status_code=200)
async def delete_product_rate(id:str,session: AsyncSession = Depends(get_session)):
    return await product_rate.delete_product_rate(id,session)
