from sqlalchemy import Boolean, Column, Float, String
from sqlalchemy.orm import relationship

from app.models.base import BaseModel


class PaymentMethod(BaseModel):
    __tablename__ = "payment_methods"

    name = Column(String, nullable=False)
    description = Column(String) #Provides additional information about the payment method.
    type = Column(String, nullable=False) #Purpose: Categorizes the payment method (e.g., Credit Card, Bank Transfer, PayPal).
    is_active = Column(Boolean, default=True) #Purpose: Indicates whether the payment method is currently active and available for use.
    transaction_fee = Column(Float, default=0.0) #Purpose: Specifies any fees associated with using this payment method.
    currency = Column(String, default='USD') #Purpose: Denotes the currency in which transactions are processed.
    provider = Column(String) #Purpose: Names the service provider or gateway (e.g., Stripe, PayPal).
    attachment_qr = Column(String)

    # Relationship back to orders
    orders = relationship("Order", back_populates="payment_method")
