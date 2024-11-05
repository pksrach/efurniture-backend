from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import category

frontend_category_router = APIRouter(
    prefix="/categories",
    responses={404: {"description": "Not Found!"}},
)

@frontend_category_router.get("", status_code=200)
async def get_categories(session: AsyncSession = Depends(get_session), pagination: PaginationParam = Depends(PaginationParam)):
    return await category.get_categories(session, pagination)