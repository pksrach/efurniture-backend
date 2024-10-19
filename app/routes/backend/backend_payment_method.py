from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import payment_method

payment_method_router = APIRouter(
    prefix="/payment_methods",
    tags=["Backend Payment Method API"],
    responses={404: {"description": "Not found"}},
)


@payment_method_router.get("", status_code=200)
async def get_payment_methods(session: AsyncSession = Depends(get_session),
                              pagination: PaginationParam = Depends(PaginationParam)):
    return await payment_method.get_payment_methods(session, pagination)


@payment_method_router.get("/{id}", status_code=200)
async def get_payment_method(id: str, session: AsyncSession = Depends(get_session)):
    return await payment_method.get_payment_method(id, session)


@payment_method_router.post("", status_code=200)
async def create_payment_method(req: payment_method.PaymentMethodRequest, session: AsyncSession = Depends(get_session)):
    return await payment_method.create_payment_method(req, session)


@payment_method_router.put("/{id}", status_code=200)
async def update_payment_method(id: str, req: payment_method.PaymentMethodRequest,
                                session: AsyncSession = Depends(get_session)):
    return await payment_method.update_payment_method(id, req, session)


@payment_method_router.delete("/{id}", status_code=200)
async def delete_payment_method(id: str, session: AsyncSession = Depends(get_session)):
    return await payment_method.delete_payment_method(id, session)
