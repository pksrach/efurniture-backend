# app/routes/seeding/seed_data.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session  # Import the session dependency
from app.config.security import get_current_user
from app.services.frontend import frontend_cart_service
from app.services.seeding import seed_base, seed_cart, seed_order

seed_router = APIRouter(
    prefix="/seeds",
    tags=["Default"],
    responses={404: {"description": "Not Found!"}},
)


@seed_router.post("", status_code=status.HTTP_201_CREATED, responses={201: {"description": "Seeded successfully"}})
async def seed_all(session: AsyncSession = Depends(get_session)):
    return await seed_base.seed_all(session)


@seed_router.post("/carts", status_code=status.HTTP_201_CREATED,
                  responses={201: {"description": "Seeded successfully"}})
async def seed_carts(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await seed_cart.SeedCart(user, session).run(frontend_cart_service.add_all_carts)


@seed_router.post("/orders", status_code=status.HTTP_201_CREATED,
                  responses={201: {"description": "Seeded successfully"}})
async def seed_orders(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await seed_order.SeedOrder(user, session).seed_order_from_carts()
