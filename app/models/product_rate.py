from sqlalchemy import Column, Date, ForeignKey, Integer, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class ProductRate(Base):
    __tablename__ = "product_rates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    rate = Column(Integer)

    user = relationship("User")
    product = relationship("Product")