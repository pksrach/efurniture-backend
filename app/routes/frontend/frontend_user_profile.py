from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_current_user, get_frontend_user
from app.services.frontend.frontend_profile_service import get_current_profile

frontend_profile_router = APIRouter(
    prefix="/profile",
    tags=["Frontend Profile API"],
    dependencies=[Depends(get_frontend_user)]
)


@frontend_profile_router.get("", status_code=200)
async def get_profile(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    print("Fetching profile for user: ", user.id)
    return await get_current_profile(user, session)
