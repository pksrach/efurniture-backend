from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_session
from app.services import category

category_router = APIRouter(
    prefix="/categories",
    tags=["Backend Category API"],
    responses={404: {"description": "Not found"}},
)


@category_router.get("", status_code=200)
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await category.get_categories(session)


@category_router.get("/{id}", status_code=200)
async def get_category(id: str, session: AsyncSession = Depends(get_session)):
    return await category.get_category(id, session)


@category_router.post("", status_code=201)
async def create_category(req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.create_category(req, session)


@category_router.put("/{id}", status_code=200)
async def update_category(id: str, req: category.CategoryRequest, session: AsyncSession = Depends(get_session)):
    return await category.update_category(id, req, session)


@category_router.delete("/{id}", status_code=200)
async def delete_category(id: str, session: AsyncSession = Depends(get_session)):
    return await category.delete_category(id, session)
