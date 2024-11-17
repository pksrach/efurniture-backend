import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.config.security import hash_password
from app.models.customer import Customer
from app.responses.customer import CustomerResponse, CustomerDataResponse
from app.responses.paginated_response import PaginationParam
from app.services.base_service import fetch_paginated_data


async def reset_password(customer_id: str, password: str, session: AsyncSession):
    try:
        # Validate and convert the id to a UUID object
        customer_uuid = uuid.UUID(customer_id)
    except ValueError:
        raise Exception("Invalid UUID format")

    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .where(Customer.id == customer_uuid)
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


async def get_customer(customer_id: str, session: AsyncSession) -> CustomerResponse:
    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .where(Customer.id == customer_id)
    )
    result = await session.execute(stmt)
    customer = result.scalar()

    if customer is None:
        raise Exception("Customer not found")

    return CustomerResponse.from_entity(customer)


async def get_customers(session: AsyncSession, pagination: PaginationParam):
    stmt = (
        select(Customer)
        .options(joinedload(Customer.user))
        .order_by(Customer.created_at.desc())
    )

    return await fetch_paginated_data(
        session=session,
        stmt=stmt,
        entity=Customer,
        pagination=pagination,
        data_response_model=CustomerDataResponse,
        order_by_field=Customer.created_at,
        message="Customers fetched successfully."
    )
