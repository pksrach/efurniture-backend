from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config.security import generate_token, verify_password, get_token_payload
from app.config.settings import get_settings
from app.models.user import User
from app.responses.auth import TokenResponse, TokenData
from app.schemas.auth import LoginRequest

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
