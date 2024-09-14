# app/routes/user.py
from fastapi import APIRouter, Depends

from app.config.security import get_current_user

user_router = APIRouter(
    prefix="/users",
    tags=["Frontend API"],
    responses={404: {"description": "Not Found!"}},
    dependencies=[Depends(get_current_user)]
)


@user_router.get("/products", status_code=200, response_model=list)
async def get_products():
    return [
        {"name": "Product 1", "price": 100},
        {"name": "Product 2", "price": 200},
        {"name": "Product 3", "price": 300},
    ]