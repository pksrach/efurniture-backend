import uuid
from math import ceil

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.pagination import PaginatedResponse
from app.config.security import hash_password
from app.config.settings import get_settings
from app.constants.gender import Genders
from app.models.customer import Customer
from app.responses.customer import CustomerListResponse, CustomerDataResponse, CustomerResponse

settings = get_settings()


async def reset_password(id: str, password: str, session: AsyncSession):
    try:
        # Validate and convert the id to a UUID object
        customer_id = uuid.UUID(id)
    except ValueError:
        raise Exception("Invalid UUID format")

    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .where(Customer.id == customer_id)
    )
    result = await session.execute(stmt)
    customer = result.scalars().first()

    if customer is None:
        raise Exception("Customer not found")

    user = customer.user

    print("Password: ", password)
    user.password = hash_password(password)
    await session.commit()

    return {
        "message": "Password reset successfully"
    }


async def get_customer(id: str, session: AsyncSession) -> CustomerResponse:
    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .where(Customer.id == id)
    )
    result = await session.execute(stmt)
    customer = result.scalars().first()

    if customer is None:
        raise Exception("Customer not found")

    return CustomerResponse(
        data=CustomerDataResponse(
            id=customer.id,
            name=customer.name,
            username=customer.user.username,
            email=customer.user.email,
            gender=Genders.get_name(customer.gender),
            phone_number=customer.phone_number,
            address=customer.address,
            active=customer.user.is_active,
            created_at=customer.created_at
        ),
        message="Customer fetched successfully"
    )


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


# Still error cannot respond with page for now
async def get_customers_with_page(session: AsyncSession, page: int, limit: int):
    offset = (page - 1) * limit

    # Query for total count of customers
    total_stmt = select(func.count(Customer.id))
    total_result = await session.execute(total_stmt)
    total_customers = total_result.scalar()

    # Query for paginated customers
    stmt = (
        select(Customer)
        .order_by(Customer.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    result = await session.execute(stmt)
    customers = result.scalars().all()

    total_pages = ceil(total_customers / limit)

    return PaginatedResponse[CustomerDataResponse](
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
        message="Customers fetched successfully",
        page=page,
        limit=limit,
        total_items=total_customers,
        total_pages=total_pages
    )
