from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.order import Order  # Ensure Order is imported

class Staff(BaseModel):
    __tablename__ = "staffs"
    name = Column(String, nullable=False)
    gender = Column(Integer)
    address = Column(String)
    phone_number = Column(String)
    salary = Column(Float)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    user = relationship("User", back_populates="staff", uselist=False)
    orders = relationship("Order", back_populates="staff")