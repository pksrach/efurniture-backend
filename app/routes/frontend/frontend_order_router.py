from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_frontend_user, get_current_user
from app.responses.paginated_response import PaginationParam
from app.schemas.order import OrderRequest
from app.services import order as backend_order_service
from app.services.frontend import frontend_order_service

frontend_order_router = APIRouter(
    prefix="/orders",
    responses={404: {"description": "Not Found!"}},
    dependencies=[Depends(get_frontend_user)]
)


@frontend_order_router.get("", status_code=200)
async def get_orders(
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam),
        user=Depends(get_current_user),
):
    return await backend_order_service.get_orders(session, pagination, user)


@frontend_order_router.get("/{order_number}", status_code=200)
async def get_order(
        order_number: str,
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user),
):
    return await backend_order_service.get_order(order_number.strip(), session, user)


@frontend_order_router.get("/details/{order_id}", status_code=200)
async def get_order_details(
        order_id: str,
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user),
):
    return await backend_order_service.get_order_details(order_id, session, user)


@frontend_order_router.post("", status_code=201)
async def checkout_order(
        req: OrderRequest,
        user=Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    return await frontend_order_service.create_order(req, user, session)


@frontend_order_router.get("/histories/{order_number}", status_code=200)
async def get_order_histories(
        order_number: str,
        session: AsyncSession = Depends(get_session),
        user=Depends(get_current_user)
):
    return await backend_order_service.get_order_histories(order_number.strip(), session, user)
