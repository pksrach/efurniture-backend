from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.responses.paginated_response import PaginationParam
from app.services import category

category_router = APIRouter(
    prefix="/categories",
    tags=["Backend Category API"],
    responses={404: {"description": "Not found"}},
)


@category_router.get("", status_code=200)
async def get_categories(
        session: AsyncSession = Depends(get_session),
        pagination: PaginationParam = Depends(PaginationParam)
):
    return await category.get_categories(session, pagination)


@category_router.get("/{category_id}", status_code=200)
async def get_category(category_id: str, session: AsyncSession = Depends(get_session)):
    return await category.get_category(category_id, session)


@category_router.post("", status_code=201)
async def create_category(req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.create_category(req, session)


@category_router.put("/{category_id}", status_code=200)
async def update_category(category_id: str, req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.update_category(category_id, req, session)


@category_router.delete("/{category_id}", status_code=200)
async def delete_category(category_id: str, session: AsyncSession = Depends(get_session)):
    return await category.delete_category(category_id, session)
