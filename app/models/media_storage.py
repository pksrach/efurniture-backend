from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.models.base import BaseModel


class MediaStorage(BaseModel):
    __tablename__ = "media_storages"

    name = Column(String, nullable=True)
    unique_name = Column(String, nullable=True)
    extension = Column(String, nullable=True)
    uri = Column(String, nullable=True)
    created_on = Column(DateTime, default=datetime.now)
    reference_id = Column(UUID(as_uuid=True), nullable=True)
    entity_type = Column(String, nullable=True)
