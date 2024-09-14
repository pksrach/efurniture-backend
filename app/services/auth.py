import random
from datetime import timedelta, datetime

import httpx
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from app.config.security import generate_token, verify_password, get_token_payload, hash_password
from app.config.settings import get_settings
from app.models.user import User
from app.models.user_token import UserToken
from app.responses.auth import TokenResponse, TokenData
from app.schemas.auth import LoginRequest, VerifyPasswordRequest, ResetNewPasswordRequest

settings = get_settings()


async def auth_login(request: LoginRequest, session: AsyncSession) -> TokenResponse:
    try:
        stmt = select(User).where(or_(User.email == request.email, User.username == request.username))
        result = await session.execute(stmt)
        user_exist = result.scalar()

        if not user_exist:
            raise HTTPException(status_code=400, detail="Email or username not found.")

        if not verify_password(request.password, user_exist.password):
            raise HTTPException(status_code=400, detail="Invalid password.")

        access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expiry = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = generate_token(user_exist.id, settings.JWT_SECRET, settings.JWT_ALGORITHM, access_token_expiry)
        refresh_token = generate_token(user_exist.id, settings.JWT_SECRET, settings.JWT_ALGORITHM, refresh_token_expiry)

        return TokenResponse(
            message="Login successful.",
            data=TokenData(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        )
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


async def auth_refresh(refresh_token: str, session: AsyncSession) -> TokenResponse:
    payload = get_token_payload(refresh_token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid refresh token.")
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid refresh token.")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(user.id, settings.JWT_SECRET, settings.JWT_ALGORITHM, access_token_expiry)

    return TokenResponse(
        message="Login successful.",
        data=TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


async def send_reset_password_email(email: str, reset_token: str):
    url = "https://sandbox.api.mailtrap.io/api/send/3138514"
    payload = {
        "from": {"email": "mailtrap@example.com", "name": "Mailtrap Test"},
        "to": [{"email": email}],
        "subject": "Password Reset Request",
        "text": f"Please use the following token to reset your password: {reset_token}",
        "category": "Integration Test"
    }
    headers = {
        "Authorization": "Bearer " + settings.MAILTRAP_TEST_TOKEN,
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
    return JSONResponse(content=response.json(), status_code=response.status_code)


async def auth_forgot_password(email: str, session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Generate a 6-digit reset code
    reset_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    # Generate a reset token
    expiry = 2  # in minutes
    reset_token = generate_token(user.id, settings.JWT_SECRET, settings.JWT_ALGORITHM, timedelta(minutes=expiry),
                                 {"code": reset_code})
    print("reset_token", reset_token)

    # Store the token in the database
    user_token = UserToken(
        user_id=user.id,
        access_key=reset_token,
        expires_at=datetime.now() + timedelta(minutes=expiry)
    )
    session.add(user_token)
    await session.commit()

    # Send the reset token via email
    await send_reset_password_email(user.email, reset_code)

    return {
        "message": "Reset code sent successfully.",
        "data": {
            "token": reset_token
        }
    }


async def auth_verify_password(req: VerifyPasswordRequest, session: AsyncSession):
    stmt = select(UserToken).where(UserToken.access_key == req.token)
    result = await session.execute(stmt)
    user_token = result.scalar()

    if not user_token:
        raise HTTPException(status_code=404, detail="Token not found.")

    if user_token.expires_at < datetime.now():
        raise HTTPException(status_code=400, detail="Token expired.")

    # Decode the token to get the code
    payload = get_token_payload(req.token, settings.JWT_SECRET, settings.JWT_ALGORITHM)

    # Before get code need to check first if the payload is not None
    if payload is None:
        raise HTTPException(status_code=400, detail="Invalid token.")

    payloadCode = payload.get("dict").get("code")

    if req.code != payloadCode:
        raise HTTPException(status_code=400, detail="Invalid code.")

    user_id = payload.get("sub")
    expiry = 5  # in minutes
    access_token = generate_token(user_id, settings.JWT_SECRET, settings.JWT_ALGORITHM, timedelta(minutes=expiry))

    return {
        "message": "Code verified successfully.",
        "data": {
            "access_token": access_token,
            "expires_in": expiry
        }
    }


async def auth_reset_new_password(user_id: int, new_password: str, session: AsyncSession):
    if not user_id:
        raise HTTPException(status_code=400, detail="User not found.")

    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.password = hash_password(new_password)
    await session.commit()

    return {
        "message": "Password reset successfully."
    }
