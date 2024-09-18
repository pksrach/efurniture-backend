from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.services import customer

customer_router = APIRouter(
    prefix="/customers",
    tags=["Backend Customer API"],
    responses={404: {"description": "Not found"}},
)


@customer_router.get("", status_code=200)
async def get_customers(session: AsyncSession = Depends(get_session)):
    return await customer.get_customers(session)

@customer_router.post("/list-paginated",status_code=200)
async def get_paginated_customers(page: int = 1, limit: int = 10,session: AsyncSession = Depends(get_session)):
    return await customer.get_paginated_customers(session,page,limit)

@customer_router.get("/{id}", status_code=200)
async def get_customer(id: str, session: AsyncSession = Depends(get_session)):
    return await customer.get_customer(id, session)


@customer_router.put("/reset_password/{id}", status_code=200)
async def reset_password(id: str, password: str, session: AsyncSession = Depends(get_session)):
    return await customer.reset_password(id, password, session)
