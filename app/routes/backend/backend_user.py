from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.services.user import get_all_users

backend_user_router = APIRouter(
    prefix="/backend/users",
    tags=["Backend User API"],
    responses={404: {"description": "Not found"}},
)


@backend_user_router.get("", status_code=200)
async def get_users(session: AsyncSession = Depends(get_session)):
    return await get_all_users(session)
