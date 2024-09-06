from sqlalchemy import Column, Date, ForeignKey, String,Float
from app.config.database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_date = Column(Date, nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))
    location_price = Column(Float)
    total = Column(Float)
    discount = Column(Float)
    amount = Column(Float)
    payment_method_id = Column(UUID(as_uuid=True), ForeignKey("payment_methods.id"))
    payment_attachment = Column(String)
    order_status = Column(String)
    note = Column(String)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"))

    customer = relationship("Customer", back_populates="orders")
    location = relationship("Location")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    staff = relationship("Staff", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")