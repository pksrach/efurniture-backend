from fastapi import APIRouter, Depends

from app.config.security import get_frontend_user
from app.routes.frontend.product import product_router
from app.routes.frontend.user import user_router

frontend_router = APIRouter(
    prefix="/frontend",
    tags=["Frontend API"],
    responses={404: {"description": "Not Found!"}},
    dependencies=[Depends(get_frontend_user)]
)

frontend_router.include_router(user_router)
frontend_router.include_router(product_router)
