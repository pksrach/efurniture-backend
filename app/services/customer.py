import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.security import hash_password
from app.config.settings import get_settings
from app.models.customer import Customer
from app.responses.customer import CustomerListResponse, CustomerResponse,CustomerDataResponse
from app.responses.paginated_response import PaginatedResponse

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
    customer = result.scalar()

    if customer is None:
        raise Exception("Customer not found")

    return CustomerResponse.from_entity(customer)

async def get_paginated_customers(session: AsyncSession, page: int = 1, limit: int = 10) -> PaginatedResponse[CustomerDataResponse]:
    offset = (page - 1) * limit
    total_items_query = await session.execute(select(func.count(Customer.id)))
    total_items = total_items_query.scalar_one()
    stmt = select(Customer).order_by(Customer.created_at.desc()).offset(offset).limit(limit)
    result = await session.execute(stmt)
    customers = result.scalars().all()
    total_pages = (total_items + limit - 1) // limit
    customer_data = [CustomerDataResponse.from_entity(customer) for customer in customers]
    
    return PaginatedResponse[CustomerDataResponse](
        data=customer_data,
        message="Customers retrieved successfully.",
        page=page,
        limit=limit,
        total_items=total_items,
        total_pages=total_pages,
    )

async def get_customers(session: AsyncSession) -> CustomerListResponse:
    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .order_by(Customer.created_at.desc())
    )
    result = await session.execute(stmt)
    customers = result.scalars().all()
    return CustomerListResponse.from_entities(list(customers))
