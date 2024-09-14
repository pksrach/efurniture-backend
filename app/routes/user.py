# app/routes/user.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.user import UserResponse
from app.schemas.user import RegisterUserRequest
from app.services import user

user_router = APIRouter(
    prefix="/users",
    tags=["Frontend API"],
    responses={404: {"description": "Not Found!"}},
)

@user_router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(data: RegisterUserRequest, session: AsyncSession = Depends(get_session)):
    return await user.create_user_account(data, session)