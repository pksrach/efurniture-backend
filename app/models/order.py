from sqlalchemy import Column, Date, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.location import Location  # Ensure Location is imported
from app.models.payment_method import PaymentMethod  # Ensure PaymentMethod is imported
from app.models.order_detail import OrderDetail  # Ensure OrderDetail is imported


class Order(BaseModel):
    __tablename__ = "orders"
    order_date = Column(Date, nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))
    location_price = Column(Float)
    amount = Column(Float)
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"))
    payment_attachment = Column(String)
    order_status = Column(String)
    note = Column(String, nullable=True)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staffs.id"), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    location = relationship("Location", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    staff = relationship("Staff", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", lazy='select')
    order_histories = relationship("OrderHistory", back_populates="order", lazy='select')