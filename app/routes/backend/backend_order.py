from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_backend_user
from app.models.user import User
from app.responses.paginated_response import PaginationParam
from app.services import order

order_router = APIRouter(
    prefix="/orders",
    tags=["Backend Order API"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_backend_user)]
)


@order_router.get("", status_code=200)
async def get_orders(session: AsyncSession = Depends(get_session),
                     pagination: PaginationParam = Depends(PaginationParam)):
    return await order.get_orders(session, pagination)


@order_router.get("/{order_id}", status_code=200)
async def get_order(order_id: str, session: AsyncSession = Depends(get_session)):
    return await order.get_order(order_id, session)


@order_router.get("/details/{order_id}", status_code=200)
async def get_order_details(order_id: str, session: AsyncSession = Depends(get_session)):
    return await order.get_order_details(order_id, session)


@order_router.post("/accept/{order_id}", status_code=200)
async def accept_order(order_id: str, session: AsyncSession = Depends(get_session), current_user: User = Depends(get_backend_user)):
    return await order.accept_order(order_id, session, current_user)
