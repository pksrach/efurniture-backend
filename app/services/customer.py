from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.settings import get_settings
from app.constants.gender import Genders
from app.models.customer import Customer
from app.responses.customer import CustomerListResponse, CustomerDataResponse

settings = get_settings()


async def get_customers(session: AsyncSession) -> CustomerListResponse:
    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .order_by(Customer.created_at.desc())
    )
    result = await session.execute(stmt)
    customers = result.scalars().all()
    return CustomerListResponse(
        data=[
            CustomerDataResponse(
                id=customer.id,
                name=customer.name,
                username=customer.user.username,
                email=customer.user.email,
                gender=Genders.get_name(customer.gender),
                phone_number=customer.phone_number,
                address=customer.address,
                active=customer.user.is_active,
                created_at=customer.created_at
            ) for customer in customers
        ],
        message="Customers fetched successfully"
    )
