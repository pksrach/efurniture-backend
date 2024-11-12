from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_frontend_user, get_current_user
from app.schemas.order import OrderRequest
from app.services.frontend import frontend_order_service as order

frontend_order_router = APIRouter(
    prefix="/orders",
    responses={404: {"description": "Not Found!"}},
    dependencies=[Depends(get_frontend_user)]
)


@frontend_order_router.post("", status_code=201)
async def checkout_order(req: OrderRequest, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await order.create_order(req, user, session)
