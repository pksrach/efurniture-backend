from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class OrderDetail(BaseModel):
    __tablename__ = "order_details"

    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"))
    color_id = Column(UUID(as_uuid=True), ForeignKey("colors.id"))
    size = Column(String, nullable=True)
    price = Column(Float)
    qty = Column(Integer)
    total = Column(Float)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")
    category = relationship("Category", back_populates="order_details")
    brand = relationship("Brand", back_populates="order_details")
    color = relationship("Color", back_populates="order_details")
