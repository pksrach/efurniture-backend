from fastapi import APIRouter

from app.routes.frontend.frontend_product import frontend_product_router
from app.routes.frontend.frontend_user_profile import frontend_profile_router

frontend_router = APIRouter(
    prefix="/frontend",
    responses={404: {"description": "Not Found!"}},
)

frontend_router.include_router(frontend_profile_router, tags=["Frontend Profile API"])
frontend_router.include_router(frontend_product_router, tags=["Frontend Product API"])
