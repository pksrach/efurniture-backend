from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import EmailStr, BaseModel

from app.constants.gender import Genders
from app.responses.base import BaseResponse


class FrontendProfileDataResponse(BaseModel):
    user_id: UUID | str
    customer_id: UUID | str
    username: str
    email: EmailStr
    name: str | None
    gender: int | str | None
    phone: str | None
    address: str | None
    created_at: Optional[Union[str, datetime]] = None

    @classmethod
    def from_entity(cls, customer):
        return cls(
            user_id=customer.user.id,
            customer_id=customer.id,
            username=customer.user.username,
            email=customer.user.email,
            name=customer.name,
            gender=Genders.get_name(customer.gender),
            phone=customer.phone_number,
            address=customer.address,
            created_at=customer.created_at
        )


class FrontendProfileResponse(BaseResponse):
    data: FrontendProfileDataResponse | None

    @classmethod
    def from_entity(cls, customer):
        if customer is None:
            return cls(
                data=None,
                message="Profile not found"
            )

        return cls(
            data=FrontendProfileDataResponse.from_entity(customer),
            message="Profile fetched successfully"
        )
