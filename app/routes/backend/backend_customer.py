from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import customer

customer_router = APIRouter(
    prefix="/customers",
    tags=["Backend Customer API"],
    responses={404: {"description": "Not found"}},
)


@customer_router.get("", status_code=200)
async def get_customers(session: AsyncSession = Depends(get_session),
                        pagination: PaginationParam = Depends(PaginationParam)):
    return await customer.get_customers(session, pagination)


@customer_router.get("/{customer_id}", status_code=200)
async def get_customer(customer_id: str, session: AsyncSession = Depends(get_session)):
    return await customer.get_customer(customer_id, session)


@customer_router.put("/reset_password/{customer_id}", status_code=200)
async def reset_password(customer_id: str, password: str, session: AsyncSession = Depends(get_session)):
    return await customer.reset_password(customer_id, password, session)
