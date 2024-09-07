from sqlalchemy import Column, String
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class PaymentMethod(Base):
    __tablename__ = "payment_methods"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    attachment_qr = Column(String)

    orders = relationship("Order", back_populates="payment_method")