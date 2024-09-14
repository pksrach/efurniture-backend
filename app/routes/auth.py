from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_current_user
from app.constants.roles import Roles
from app.responses.auth import TokenResponse
from app.responses.user import UserResponse, UserDataResponse
from app.schemas.auth import LoginRequest
from app.schemas.user import ResetRequest
from app.services import auth
from app.services import user

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth API"],
    responses={404: {"description": "Not found"}},
)


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def login(req: LoginRequest, session: AsyncSession = Depends(get_session)):
    return await auth.auth_login(req, session)


@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh(refresh_token: str = Header(None), session: AsyncSession = Depends(get_session)):
    return await auth.auth_refresh(refresh_token, session)


@guest_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def me(user: UserDataResponse = Depends(get_current_user)):
    return UserResponse(
        data=UserDataResponse(
            id=str(user.id),
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=Roles.get_name(user.role),
            created_at=user.created_at,
        ),
        message="User fetched successfully"
    )


@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: AsyncSession = Depends(get_session)):
    await user.reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})
