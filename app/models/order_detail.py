from sqlalchemy import Column,ForeignKey, Integer, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_price_id = Column(UUID(as_uuid=True), ForeignKey("product_prices.id"))
    price = Column(Float)
    qty = Column(Integer)
    total = Column(Float)
    discount = Column(Float)
    amount = Column(Float)

    order = relationship("Order", back_populates="order_details")
    product_price = relationship("ProductPrice", back_populates="order_details")