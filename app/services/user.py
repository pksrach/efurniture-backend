import logging
from datetime import datetime, timedelta

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.config.security import generate_token, get_token_payload, hash_password, is_password_strong_enough, load_user, \
    str_decode, str_encode, verify_password
from app.config.settings import get_settings
from app.models.customer import Customer
from app.models.user import User
from app.models.user_token import UserToken
from app.schemas.user import RegisterUserRequest, ResetRequest
from app.utils.email_context import FORGOT_PASSWORD
from app.utils.string import unique_string

settings = get_settings()


async def create_user_account(data: RegisterUserRequest, session: AsyncSession):
    try:
        async with session.begin():
            stmt = select(User).filter(User.email == data.email)
            result = await session.execute(stmt)
            user_exist = result.scalars().first()

            if user_exist:
                raise HTTPException(status_code=400, detail="Email or username already exists.")

            if not is_password_strong_enough(data.password):
                raise HTTPException(status_code=400, detail="Please provide a strong password.")

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
                address=None,
                phone=None,
            )

            session.add(new_customer)
            await session.flush()

        await session.commit()
        await session.refresh(new_user)
        return new_user

    except Exception as e:
        logging.exception(e)
        await session.rollback()
        raise HTTPException(status_code=400, detail="Invalid Request: " + str(e))


async def get_login_token(data: OAuth2PasswordRequestForm, session: AsyncSession):
    user_exist = await load_user(data.username, session)

    if not user_exist:
        raise HTTPException(status_code=400, detail="Email is not registered with us.")

    if not verify_password(data.password, user_exist.password):
        raise HTTPException(status_code=400, detail="Invalid Email or Password")

    # Generate the JWT Token
    return await _generate_tokens(user_exist, session)


async def get_refresh_token(refresh_token: str, session: AsyncSession):
    token_payload = await get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    if not token_payload:
        raise HTTPException(status_code=400, detail="Invalid Request.")

    refresh_key = token_payload.get('t')
    access_key = token_payload.get('a')
    user_id = int(str_decode(token_payload.get('sub')))

    stmt = select(UserToken).options(joinedload(UserToken.user)).filter(
        UserToken.refresh_key == refresh_key,
        UserToken.access_key == access_key,
        UserToken.user_id == user_id,
        UserToken.expires_at > datetime.now()
    )
    result = await session.execute(stmt)
    user_token = result.scalars().first()

    if not user_token:
        raise HTTPException(status_code=400, detail="Invalid Request.")

    user_token.expires_at = datetime.now()
    session.add(user_token)
    await session.commit()
    return await _generate_tokens(user_token.user, session)


async def _generate_tokens(user, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.now() + rt_expires
    session.add(user_token)
    await session.commit()
    await session.refresh(user_token)

    at_payload = {
        "sub": str_encode(str(user.id)),
        'a': access_key,
        'r': str_encode(str(user_token.id)),
        'n': str_encode(f"{user.username}")
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, 'a': access_key}
    refresh_token = generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "expires_in": at_expires.seconds
    }


async def reset_user_password(data: ResetRequest, session: AsyncSession):
    user_exist = await load_user(data.email, session)
    if not user_exist:
        raise HTTPException(status_code=400, detail="Invalid request")

    user_token = user_exist.get_context_string(context=FORGOT_PASSWORD)
    try:
        token_valid = verify_password(user_token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False

    if not token_valid:
        raise HTTPException(status_code=400, detail="Invalid token.")

    user_exist.password = hash_password(data.password)
    user_exist.updated_at = datetime.now()
    session.add(user_exist)
    await session.commit()
    await session.refresh(user_exist)
    return {"message": "Password reset completed"}


async def fetch_user_detail(pk: int, session: AsyncSession):
    stmt = select(User).filter(User.id == pk)
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user:
        return user
    raise HTTPException(status_code=400, detail="User does not exist.")
