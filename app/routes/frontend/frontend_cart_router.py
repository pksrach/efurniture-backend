from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_frontend_user, get_current_user
from app.schemas.cart import CartRequest
from app.services.frontend import frontend_cart_service as cart

frontend_cart_router = APIRouter(
    prefix="/carts",
    responses={404: {"description": "Not Found!"}},
    dependencies=[Depends(get_frontend_user)]
)


@frontend_cart_router.get("", status_code=200)
async def get_carts(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await cart.get_carts(user, session)

@frontend_cart_router.post("", status_code=201)
async def add_cart(req: CartRequest, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await cart.add_cart(req, user, session)