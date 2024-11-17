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


@order_router.get("/{order_id_or_number}", status_code=200)
async def get_order(order_id_or_number: str, session: AsyncSession = Depends(get_session)):
    return await order.get_order(order_id_or_number.strip(), session)


@order_router.get("/details/{order_id}", status_code=200)
async def get_order_details(order_id: str, session: AsyncSession = Depends(get_session)):
    return await order.get_order_details(order_id.strip(), session)


@order_router.put("/accept/{order_id}", status_code=200)
async def accept_order(order_id: str, session: AsyncSession = Depends(get_session),
                       current_user: User = Depends(get_backend_user)):
    return await order.process_order(order_id.strip(), "accepted", session, current_user)


@order_router.put("/delivery/{order_id}", status_code=200)
async def delivery_order(order_id: str, session: AsyncSession = Depends(get_session),
                         current_user: User = Depends(get_backend_user)):
    return await order.process_order(order_id.strip(), "delivered", session, current_user)


@order_router.put("/done/{order_id}", status_code=200)
async def done_order(order_id: str, session: AsyncSession = Depends(get_session),
                     current_user: User = Depends(get_backend_user)):
    return await order.process_order(order_id.strip(), "done", session, current_user)


@order_router.delete("/cancel/{order_id}", status_code=200)
async def cancel_order(order_id: str, session: AsyncSession = Depends(get_session),
                       current_user: User = Depends(get_backend_user)):
    return await order.process_order(order_id.strip(), "canceled", session, current_user)


@order_router.get("/histories/{order_id_or_number}", status_code=200)
async def get_orders(order_id_or_number, session: AsyncSession = Depends(get_session)):
    return await order.get_order_histories(order_id_or_number.strip(), session)
