from fastapi import APIRouter

from app.routes.frontend.frontend_brand_router import frontend_brand_router
from app.routes.frontend.frontend_cart_router import frontend_cart_router
from app.routes.frontend.frontend_category_router import frontend_category_router
from app.routes.frontend.frontend_color_router import frontend_color_router
from app.routes.frontend.frontend_location_router import frontend_location_router
from app.routes.frontend.frontend_order_router import frontend_order_router
from app.routes.frontend.frontend_product_router import frontend_product_router
from app.routes.frontend.frontend_user_profile_router import frontend_profile_router

frontend_router = APIRouter(
    prefix="/frontend",
    responses={404: {"description": "Not Found!"}},
)

frontend_router.include_router(frontend_profile_router, tags=["Frontend Profile API"])
frontend_router.include_router(frontend_product_router, tags=["Frontend Product API"])
frontend_router.include_router(frontend_category_router, tags=["Frontend Category API"])
frontend_router.include_router(frontend_brand_router, tags=["Frontend Brand API"])
frontend_router.include_router(frontend_color_router, tags=["Frontend Color API"])
frontend_router.include_router(frontend_cart_router, tags=["Frontend Cart API"])
frontend_router.include_router(frontend_order_router, tags=["Frontend Order API"])
frontend_router.include_router(frontend_location_router, tags=["Frontend Location API"])
