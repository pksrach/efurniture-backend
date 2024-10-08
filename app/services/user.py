import logging
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.custom_exceptions import CustomHTTPException
from app.config.security import hash_password, is_password_long_enough, generate_token
from app.config.settings import get_settings
from app.models.customer import Customer
from app.models.user import User
from app.responses.auth import TokenResponse, TokenData
from app.responses.paginated_response import PaginationParam
from app.responses.user import UserDataResponse
from app.schemas.user import RegisterUserRequest
from app.services.base_service import fetch_paginated_data

settings = get_settings()


async def create_user_account(data: RegisterUserRequest, session: AsyncSession):
    try:
        # validate
        if not data.email:
            raise CustomHTTPException(status_code=400, message="Email is required.")

        if not data.username:
            raise CustomHTTPException(status_code=400, message="Username is required.")

        if not data.password:
            raise CustomHTTPException(status_code=400, message="Password is required.")

        async with session.begin():
            stmt = select(User).where(or_(User.email == data.email, User.username == data.username))
            result = await session.execute(stmt)
            user_exist = result.scalars().first()

            if user_exist:
                raise CustomHTTPException(status_code=400, message="Email or username already exists.")

            if not is_password_long_enough(data.password):
                raise CustomHTTPException(status_code=400, message="Please provide long password.")

            new_user = User(
                username=data.username,
                email=data.email,
                password=hash_password(data.password),
                role=0,  # Default role is 0 = Customer, 1 = User, 2 = Admin, 3 = Super Admin
                is_active=True,
                updated_at=datetime.now()
            )

            session.add(new_user)
            await session.flush()  # Ensure new_user.id is available

            # Create a customer record
            new_customer = Customer(
                user_id=new_user.id,
                name=data.username.capitalize(),
                gender=2,  # Default other
            )

            session.add(new_customer)
            await session.flush()

        await session.commit()
        await session.refresh(new_user)

        if new_user is None:
            raise CustomHTTPException(status_code=400, message="User not created.")

        access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expiry = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = generate_token(new_user, access_token_expiry)
        refresh_token = generate_token(new_user, refresh_token_expiry)

        return TokenResponse(
            message="Register successful.",
            data=TokenData(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )

    except Exception as e:
        logging.exception(e)
        await session.rollback()
        raise CustomHTTPException(status_code=400, message="Invalid Request: " + str(e))


async def get_all_users(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=User,
        pagination=pagination,
        data_response_model=UserDataResponse,
        order_by_field=User.created_at,
        message="Users fetched successfully."
    )
