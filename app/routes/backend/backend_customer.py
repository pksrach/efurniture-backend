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
