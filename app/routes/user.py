# app/routes/user.py
from fastapi import APIRouter, Depends, Header, status
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.config.security import get_current_user, bearer_token
from app.responses.user import UserResponse
from app.schemas.user import RegisterUserRequest
from app.services import user

user_router = APIRouter(
    prefix="/users",
    tags=["Frontend API"],
    responses={404: {"description": "Not Found!"}},
)

auth_router = APIRouter(
    prefix="/users",
    tags=["Frontend API"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(bearer_token), Depends(get_current_user)]
)


@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, session: AsyncSession = Depends(get_session)):
    return await user.create_user_account(data, session)


# @guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
# async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
#     return await user.get_login_token(data, session)


# @guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
# async def user_login(refresh_token=Header(), session: AsyncSession = Depends(get_session)):
#     return await user.get_refresh_token(refresh_token, session)
#
#
# @guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
# async def reset_password(data: ResetRequest, session: AsyncSession = Depends(get_session)):
#     await user.reset_user_password(data, session)
#     return JSONResponse({"message": "Your password has been updated."})


# @guest_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
# async def fetch_user(user=Depends(get_current_user)):
#     return user


@auth_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_info(
    pk: int,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    return await user.fetch_user_detail(pk, session)
