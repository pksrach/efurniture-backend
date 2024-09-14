from fastapi import APIRouter, Depends

from app.config.security import get_current_user
from app.routes.backend.category import category_router

backend_router = APIRouter(
    prefix="/backend",
    tags=["Backend API"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)]
)

backend_router.include_router(category_router)
