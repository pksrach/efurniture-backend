from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.constants.gender import Genders
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

    @classmethod
    def from_entity(cls, customer) -> 'CustomerDataResponse':
        if customer is None:
            return cls(
                id="",
                name="",
                username="",
                email="",
                gender="",
                phone_number="",
                address="",
                active=False,
                created_at=None
            )

        return cls(
            id=customer.id,
            name=customer.name,
            username=customer.username,
            email=customer.email,
            gender=Genders.get_name(customer.gender),
            phone_number=customer.phone_number,
            address=customer.address,
            active=customer.is_active,
            created_at=customer.created_at
        )


class CustomerResponse(BaseResponse):
    data: CustomerDataResponse | None

    @classmethod
    def from_entity(cls, customer) -> 'CustomerResponse':
        if customer is None:
            return cls(
                data=None,
                message="Customer not found"
            )

        return cls(
            data=CustomerDataResponse.from_entity(customer),
            message="Customer fetched successfully"
        )


class CustomerListResponse(BaseResponse):
    data: list[CustomerDataResponse]

    @classmethod
    def from_entities(cls, customers) -> 'CustomerListResponse':
        return cls(
            data=[CustomerDataResponse.from_entity(customer) for customer in customers],
            message="Customers fetched successfully"
        )
