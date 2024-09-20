from typing import Optional
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.media_storage import MediaStorage,MediaStorageDataResponse,MediaStorageListResponse,MediaStorageResponse

from app.services import category
from app.services import media_storage

category_router = APIRouter(
    prefix="/categories",
    tags=["Backend Category API"],
    responses={404: {"description": "Not found"}},
)


@category_router.get("", status_code=200)
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await category.get_categories(session)

@category_router.post("/list-paginated",status_code=200)
async def get_paginated_categories(page: int = 1, limit: int = 10,session: AsyncSession = Depends(get_session)):
    return await category.get_paginated_categories(session,page,limit)

@category_router.get("/{id}", status_code=200)
async def get_category(id: str, session: AsyncSession = Depends(get_session)):
    return await category.get_category(id, session)


@category_router.post("", status_code=201)
async def create_category(req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.create_category(req, session)


@category_router.put("/{id}", status_code=200)
async def update_category(id: str, req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.update_category(id, req, session)


@category_router.delete("/{id}", status_code=200)
async def delete_category(id: str, session: AsyncSession = Depends(get_session)):
    return await category.delete_category(id, session)

@category_router.post("/upload-file-category", status_code=200)
async def post_image_category(
    file: UploadFile,
    entity_type: Optional[str],
    reference_id: Optional[str],
    session: AsyncSession = Depends(get_session)
):
    try:
        return await media_storage.post_file(session, file,"Category", reference_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@category_router.get("/get-all-media-storage-by-ref-id/{reference_id}/{entity_type}",status_code=200)
async def get_all_media_storage_by_ref_id(reference_id: str,entity_type: Optional[str],session: AsyncSession = Depends(get_session)):
    media_storages = await media_storage.get_all_media_storage_by_ref_id(session,reference_id, entity_type)

    if not media_storages:
        raise HTTPException(status_code=404, detail="Media storage not found.")
    
    return media_storages

@category_router.get("/get-media-storage-by-ref-id/{reference_id}/{entity_type}",status_code=200)
async def get_media_storage_by_ref_id(reference_id: str,entity_type: Optional[str],session: AsyncSession = Depends(get_session)):
    media = await media_storage.get_media_storage_by_ref_id(session,reference_id, entity_type)

    if not media:
        raise HTTPException(status_code=404, detail="Media storage not found.")

    return media

@category_router.get("/get-all-media-storage-by-entity-type/{entity_type}",status_code=200)
async def get_all_media_storage_by_entity_type(entity_type: Optional[str],session: AsyncSession = Depends(get_session)):
    media_storages = await media_storage.get_all_media_storage_by_entity_type(session,entity_type)

    if not media_storages:
        raise HTTPException(status_code=404, detail="Media storage not found.")
    
    return media_storages

@category_router.delete("/delete-media-storage/{id}", status_code=200)
async def delete_media_storage(id: str, session: AsyncSession = Depends(get_session)):
    return await media_storage.delete_media_storage_by_id(id,session)