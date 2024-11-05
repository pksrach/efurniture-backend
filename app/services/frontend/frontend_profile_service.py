from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from app.config.database import get_session
from app.config.security import get_current_user
from app.models.customer import Customer
from app.responses.frontend.frontend_profile_response import FrontendProfileResponse


async def get_current_profile(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    try:
        # Fetch customer data
        stmt = (
            select(Customer)
            .options(joinedload(Customer.user))
            .where(Customer.user_id == user.id)
        )
        result = await session.execute(stmt)
        customer_data = result.scalar()

        if customer_data is None:
            raise Exception("Profile not found")

        # Ensure address field is included
        if not hasattr(customer_data, 'address'):
            raise Exception("Address not found in profile data")

        return FrontendProfileResponse.from_entity(customer_data)
    except Exception as e:
        return FrontendProfileResponse(
            data=None,
            message=str(e)
        )
