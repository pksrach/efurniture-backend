from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class OrderHistory(BaseModel):
    __tablename__ = "order_histories"
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    order_status = Column(String)

    order = relationship("Order", back_populates="order_histories")
