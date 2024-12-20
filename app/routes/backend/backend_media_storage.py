from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import media_storage

media_router = APIRouter(
    prefix="/media-storage",
    tags=["Backend Media Storage API"],
    responses={404: {"description": "Not found"}},
)


@media_router.get("", status_code=200)
async def get_media_storages(
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    return await media_storage.get_all_media_storage(session, pagination)


@media_router.get("/{media_id}", status_code=200)
async def get_media_storage(media_id, session: AsyncSession = Depends(get_session)):
    return await media_storage.get_media_storage(media_id, session)


@media_router.post("", status_code=201)
async def add_media_storage(
        file: UploadFile,
        request: Request,
        session: AsyncSession = Depends(get_session),
        namespace: Optional[str] = None,
        reference_id: Optional[UUID] = None,
):
    return await media_storage.add_media_storage(file, namespace, reference_id, request, session)


@media_router.delete("/{media_id}", status_code=200)
async def delete_media_storage(media_id: UUID, session: AsyncSession = Depends(get_session)):
    return await media_storage.delete_media_storage_by_id(media_id, session)


@media_router.delete("", status_code=200)
async def delete_media_storages(session: AsyncSession = Depends(get_session)):
    return await media_storage.delete_all_media_storage(session)
