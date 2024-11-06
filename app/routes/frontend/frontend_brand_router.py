from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import brand

frontend_brand_router = APIRouter(
    prefix="/brands",
    responses={404: {"description": "Not Found!"}},
)

@frontend_brand_router.get("", status_code=200)
async def get_brands(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await brand.get_brands(session, pagination)