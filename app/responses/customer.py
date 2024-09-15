from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.responses.base import BaseResponse


class CustomerDataResponse(BaseModel):
    id: str | UUID
    name: str
    username: str
    email: EmailStr
    gender: str | None
    phone_number: str | None
    address: str | None
    active: bool
    created_at: datetime | None


class CustomerResponse(BaseResponse):
    data: CustomerDataResponse | None


class CustomerListResponse(BaseResponse):
    data: list[CustomerDataResponse]
