import logging
import os
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import UploadFile, HTTPException, Request
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.responses.media_storage import MediaStorage, MediaStorageDataResponse, MediaStorageListResponse, \
    MediaStorageResponse
from app.responses.paginated_response import PaginationParam
from app.schemas.media_storage import MediaStorageResponseSchema
from app.services.base_service import fetch_paginated_data
from app.utils.common import is_valid_file_type, get_file_path

logger = logging.getLogger(__name__)


async def get_all_media_storage(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=MediaStorage,
        pagination=pagination,
        data_response_model=MediaStorageDataResponse,
        order_by_field=MediaStorage.created_on,
        message="Media storage fetched successfully"
    )


async def get_media_storage(id: UUID, session: AsyncSession):
    media_storage = await session.get(MediaStorage, id)
    if not media_storage:
        raise HTTPException(status_code=404, detail="Media storage not found.")
    return media_storage


async def add_media_storage(file: UploadFile, entity_type: Optional[str], reference_id: UUID, request: Request,
                            session: AsyncSession) -> MediaStorageResponseSchema:
    # Max file size is 3MB
    max_file_size = 3 * 1024 * 1024

    contents = await file.read()
    file_size = len(contents)

    if file_size > max_file_size:
        raise HTTPException(status_code=400, detail="File size exceeds the maximum limit of 3MB.")

    file_extension = os.path.splitext(file.filename)[1]
    if not is_valid_file_type(file_extension):
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, and PNG are allowed.")

    unique_name = f"{uuid.uuid4()}{file_extension}"
    file_path = get_file_path(unique_name)

    # Create the MediaStorage object
    base_url = str(request.base_url)
    media_storage = MediaStorage(
        id=uuid.uuid4(),
        unique_name=unique_name,
        name=file.filename,
        extension=file_extension,
        uri=f"{base_url}uploads/{unique_name}",
        entity_type=entity_type,
        reference_id=reference_id,
        created_on=datetime.now(),
    )

    try:
        # Save the file to the file system
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        # Add media storage record to the database
        session.add(media_storage)
        await session.commit()
        await session.refresh(media_storage)

        return media_storage

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Failed processing file {file.filename}. {str(ex)}")


async def get_all_media_storage_by_ref_id(session: AsyncSession, reference_id: UUID,
                                          entity_type: Optional[str]) -> MediaStorageListResponse:
    query = (
        select(MediaStorage)
        .where(
            and_(
                MediaStorage.reference_id == reference_id,
                MediaStorage.entity_type == entity_type,
            )
        )
    )
    result = await session.execute(query)
    media_storages = result.scalars().all()
    return MediaStorageListResponse.from_entities(list(media_storages))


async def get_media_storage_by_ref_id(session: AsyncSession, reference_id: UUID,
                                      entity_type: Optional[str]) -> MediaStorageResponse:
    query = (
        select(MediaStorage)
        .where(
            and_(
                MediaStorage.reference_id == reference_id,
                MediaStorage.entity_type == entity_type,
            )
        )
    )
    result = await session.execute(query)
    media_storage = result.scalars().first()
    return media_storage


async def find_media_storage_by_id(id: UUID, session: AsyncSession) -> MediaStorageResponse:
    return await session.get(MediaStorage, id)


async def get_all_media_storage_by_entity_type(session: AsyncSession,
                                               entity_type: Optional[str]) -> MediaStorageListResponse:
    if not entity_type:
        raise HTTPException(status_code=400, detail="Entity type cannot be null or empty.")

    query = (
        select(MediaStorage)
        .where(
            and_(
                MediaStorage.entity_type == entity_type,
            )
        )
    )
    result = await session.execute(query)
    media_storages = result.scalars().all()
    return media_storages


async def delete_media_storage_by_id(id: UUID, session: AsyncSession) -> str:
    media_storage = await session.get(MediaStorage, id)
    if not media_storage:
        raise HTTPException(status_code=404, detail="Media storage not found.")
    await session.delete(media_storage)
    await session.commit()
    return f"Media storage {id} deleted successfully"
