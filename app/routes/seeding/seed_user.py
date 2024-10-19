# app/routes/seeding/seed_user.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session  # Import the session dependency
from app.services.seeding.seed_user import SeedUser

seed_user_router = APIRouter(
    prefix="/seed/users",
    tags=["Default"],
    responses={404: {"description": "Not Found!"}},
)


@seed_user_router.post("", status_code=status.HTTP_201_CREATED, responses={201: {"description": "Seeded successfully"}})
async def seed_users(session: AsyncSession = Depends(get_session)):  # Use session dependency here
    return await SeedUser(session).run()
