# app/routes/seeding/seed_data.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session  # Import the session dependency
from app.services.seeding import seed_base

seed_router = APIRouter(
    prefix="/seed",
    tags=["Default"],
    responses={404: {"description": "Not Found!"}},
)


@seed_router.post("/all", status_code=status.HTTP_201_CREATED, responses={201: {"description": "Seeded successfully"}})
async def seed_all(session: AsyncSession = Depends(get_session)):
    return await seed_base.seed_all(session)
