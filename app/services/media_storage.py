import os
import uuid
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import get_settings
from app.models.media_storage import MediaStorage
from app.schemas.media_storage import MediaStorageCreate,MediaStorageResponse
from app.utils.common import is_valid_file_type,get_file_path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
settings = get_settings()

async def post_file(session: AsyncSession,file: UploadFile, entity_type: Optional[str],reference_id: UUID)-> MediaStorageResponse:
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
    media_storage = MediaStorage(
        id=uuid.uuid4(),
        unique_name=unique_name,
        name=file.filename,
        extension=file_extension,
        uri=f"uploads/{unique_name}",
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