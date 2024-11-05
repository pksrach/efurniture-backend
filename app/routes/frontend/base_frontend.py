from fastapi import APIRouter

from app.routes.frontend.frontend_category_router import frontend_category_router
from app.routes.frontend.frontend_product_router import frontend_product_router
from app.routes.frontend.frontend_user_profile_router import frontend_profile_router

frontend_router = APIRouter(
    prefix="/frontend",
    responses={404: {"description": "Not Found!"}},
)

frontend_router.include_router(frontend_profile_router, tags=["Frontend Profile API"])
frontend_router.include_router(frontend_product_router, tags=["Frontend Product API"])
frontend_router.include_router(frontend_category_router, tags=["Frontend Category API"])
