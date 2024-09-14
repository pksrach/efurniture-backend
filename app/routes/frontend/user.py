# app/routes/user.py
from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user",
)


@user_router.get("/profile", status_code=200, response_model=list)
async def get_profile():
    return [
        {"name": "User 1", "email": "test@gmail.com"}
    ]
