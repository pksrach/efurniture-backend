from sqlalchemy import Column, ForeignKey, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Location(Base):
    __tablename__ = "locations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    price = Column(Float)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))

    children = relationship("Location")