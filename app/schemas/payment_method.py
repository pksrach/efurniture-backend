from typing import Optional
from pydantic import BaseModel, Field

class PaymentMethodRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    is_active: Optional[bool] = None
    transaction_fee: Optional[float] = None
    currency: Optional[str] = None
    provider: Optional[str] = None
    attachment_qr: Optional[str] = None