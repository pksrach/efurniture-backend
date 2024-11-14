from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_frontend_user
from app.responses.paginated_response import PaginationParam
from app.services import location

frontend_location_router = APIRouter(
    prefix="/locations",
    dependencies=[Depends(get_frontend_user)],
    responses={404: {"description": "Not Found!"}},
)


@frontend_location_router.get("", status_code=200)
async def get_locations(session: AsyncSession = Depends(get_session),
                        pagination: PaginationParam = Depends(PaginationParam)):
    return await location.get_locations(session, pagination)


@frontend_location_router.get("/location_id", status_code=200)
async def get_location(location_id, session: AsyncSession = Depends(get_session)):
    return await location.get_location(location_id, session)
