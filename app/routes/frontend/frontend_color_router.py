from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import color

frontend_color_router = APIRouter(
    prefix="/colors",
    responses={404: {"description": "Not Found!"}},
)

@frontend_color_router.get("", status_code=200)
async def get_colors(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await color.get_colors(session, pagination)
