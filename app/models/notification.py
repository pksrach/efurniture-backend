from sqlalchemy import Column, Date, ForeignKey, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    description = Column(String)
    date = Column(Date)
    type = Column(String)

    from_user = relationship("User", foreign_keys=[from_user_id])
    to_user = relationship("User", foreign_keys=[to_user_id])