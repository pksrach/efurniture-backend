from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import payment_method

frontend_payment_method_router = APIRouter(
    prefix="/payment_methods",
    responses={404: {"description": "Not Found!"}},
)


@frontend_payment_method_router.get("", status_code=200)
async def get_payments(session: AsyncSession = Depends(get_session),
                       pagination: PaginationParam = Depends(PaginationParam)):
    return await payment_method.get_payment_methods(session, pagination)


@frontend_payment_method_router.get("/{payment_method_id}", status_code=200)
async def get_payment(payment_method_id, session: AsyncSession = Depends(get_session)):
    return await payment_method.get_payment_method(payment_method_id, session)
