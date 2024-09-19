from uuid import UUID
from pydantic import BaseModel
from app.models.media_storage import MediaStorage
from app.responses.base import BaseResponse
from datetime import datetime

class MediaStorageDataResponse(BaseModel):
    id: str | UUID
    name: str | None
    unique_name: str | None
    extension: str | None
    uri: str | None
    created_on: datetime
    reference_id: str | UUID | None
    entity_type: str | None

    @classmethod
    def from_entity(cls, media_storage: 'MediaStorage') -> 'MediaStorageDataResponse':
        if media_storage is None:
            return cls(
                id="",
                name=None,
                unique_name=None,
                extension=None,
                uri=None,
                created_on=datetime.now(),
                reference_id=None,
                entity_type=None
            )

        return cls(
            id=media_storage.id,
            name=media_storage.name,
            unique_name=media_storage.unique_name,
            extension=media_storage.extension,
            uri=media_storage.uri,
            created_on=media_storage.created_on,
            reference_id=media_storage.reference_id,
            entity_type=media_storage.entity_type
        )


class MediaStorageResponse(BaseResponse):
    data: MediaStorageDataResponse | None

    @classmethod
    def from_entity(cls, media_storage: 'MediaStorage') -> 'MediaStorageResponse':
        if media_storage is None:
            return cls(
                data=None,
                message="Media storage not found"
            )

        return cls(
            data=MediaStorageDataResponse.from_entity(media_storage),
            message="Media storage fetched successfully"
        )


class MediaStorageListResponse(BaseResponse):
    data: list[MediaStorageDataResponse]

    @classmethod
    def from_entities(cls, media_storages: list['MediaStorage']) -> 'MediaStorageListResponse':
        return cls(
            data=[MediaStorageDataResponse.from_entity(media_storage) for media_storage in media_storages],
            message="Media storages fetched successfully"
        )

