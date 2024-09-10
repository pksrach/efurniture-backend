from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel
from app.models.product_price import ProductPrice # Ensure ProductPrice is imported


class OrderDetail(BaseModel):
    __tablename__ = "order_details"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_price_id = Column(UUID(as_uuid=True), ForeignKey("product_prices.id"))
    price = Column(Float)
    qty = Column(Integer)
    total = Column(Float)
    discount = Column(Float)
    amount = Column(Float)

    order = relationship("Order", back_populates="order_details")
    product_price = relationship("ProductPrice", back_populates="order_details")
