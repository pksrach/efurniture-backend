from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import location

location_router = APIRouter(
    prefix="/locations",
    tags=["Backend Location API"],
    responses={404: {"description": "Not found"}},
)


@location_router.get("", status_code=200)
async def get_locations(session: AsyncSession = Depends(get_session),
                        pagination: PaginationParam = Depends(PaginationParam)):
    return await location.get_locations(session, pagination)


@location_router.get("/{location_id}", status_code=200)
async def get_location(location_id: str, session: AsyncSession = Depends(get_session)):
    return await location.get_location(location_id, session)


@location_router.post("", status_code=200)
async def create_location(req: location.LocationRequest, session: AsyncSession = Depends(get_session)):
    return await location.create_location(req, session)


@location_router.put("/{location_id}", status_code=200)
async def update_location(location_id: str, req: location.LocationRequest, session: AsyncSession = Depends(get_session)):
    return await location.update_location(location_id, req, session)


@location_router.delete("/{location_id}", status_code=200)
async def delete_location(location_id: str, session: AsyncSession = Depends(get_session)):
    return await location.delete_location(location_id, session)
