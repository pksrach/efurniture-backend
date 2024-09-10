from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"

    name = Column(String, nullable=False)
    attachment_qr = Column(String)

    # Relationship back to orders
    orders = relationship("Order", back_populates="payment_method")
