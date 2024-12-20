from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import color

color_router = APIRouter(
    prefix="/colors",
    tags=["Backend Color API"],
    responses={404: {"description": "Not found"}},
)


@color_router.get("", status_code=200)
async def get_colors(session: AsyncSession = Depends(get_session),
                     pagination: PaginationParam = Depends(PaginationParam)):
    return await color.get_colors(session, pagination)


@color_router.get("/{color_id}", status_code=200)
async def get_color(color_id: str, session: AsyncSession = Depends(get_session)):
    return await color.get_color(color_id, session)


@color_router.post("", status_code=201)
async def create_color(req: color.ColorRequest, session: AsyncSession = Depends(get_session)):
    return await color.create_color(req, session)


@color_router.put("/{color_id}", status_code=200)
async def update_color(color_id: str, req: color.ColorRequest, session: AsyncSession = Depends(get_session)):
    return await color.update_color(color_id, req, session)


@color_router.delete("/{color_id}", status_code=200)
async def delete_color(color_id: str, session: AsyncSession = Depends(get_session)):
    return await color.delete_color(color_id, session)
