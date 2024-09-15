from fastapi import APIRouter, Depends

from app.config.security import get_backend_user
from app.routes.backend.backend_brand import brand_router
from app.routes.backend.backend_category import category_router
from app.routes.backend.backend_color import color_router
from app.routes.backend.backend_customer import customer_router
from app.routes.backend.backend_product import product_router
from app.routes.backend.backend_user import backend_user_router

backend_router = APIRouter(
    prefix="/backend",
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_backend_user)]
)

backend_router.include_router(category_router)
backend_router.include_router(backend_user_router)
backend_router.include_router(brand_router)
backend_router.include_router(customer_router)
backend_router.include_router(color_router)
backend_router.include_router(product_router)
