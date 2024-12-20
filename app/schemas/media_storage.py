from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class MediaStorageCreate(BaseModel):
    name: Optional[str]
    unique_name: Optional[str]
    extension: Optional[str]
    uri: Optional[str]
    reference_id: Optional[UUID]
    entity_type: Optional[str]


class MediaStorageResponseSchema(BaseModel):
    id: UUID
    name: Optional[str]
    unique_name: Optional[str]
    extension: Optional[str]
    uri: Optional[str]
    created_on: datetime
    reference_id: Optional[UUID]
    entity_type: Optional[str]

    class Config:
        from_attributes = True
