import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Staff(Base):
    __tablename__ = "staffs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    gender = Column(Integer)
    address = Column(String)
    phone_number = Column(String)
    salary = Column(Float)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    user = relationship("User", back_populates="staffs")
    orders = relationship("Order", back_populates="staffs")