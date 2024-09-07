from sqlalchemy import Column, ForeignKey, Integer, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Staff(Base):
    __tablename__ = "staff"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    gender = Column(Integer)
    address = Column(String)
    phone_number = Column(String)
    salary = Column(Float)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    user = relationship("User", back_populates="staff")
    orders = relationship("Order", back_populates="staff")