from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.color import Color
from app.responses.color import ColorDataResponse, ColorResponse
from app.responses.paginated_response import PaginationParam
from app.schemas.color import ColorRequest
from app.services.base_service import fetch_paginated_data


async def get_colors(session: AsyncSession, pagination: PaginationParam):
    return await fetch_paginated_data(
        session=session,
        entity=Color,
        pagination=pagination,
        data_response_model=ColorDataResponse,
        order_by_field=Color.created_at,
        message="Colors fetched successfully"
    )


async def get_color(color_id: str, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == color_id)
    result = await session.execute(stmt)
    color = result.scalar()

    if color is None:
        return ColorResponse(
            data=None,
            message="Color not found"
        )

    return ColorResponse.from_entity(color)


async def create_color(req: ColorRequest, session: AsyncSession) -> ColorResponse:
    # Check exists name or not
    stmt = select(Color).where(Color.name == req.name)
    result = await session.execute(stmt)
    color = result.scalars().first()
    if color:
        return ColorResponse(
            data=ColorDataResponse.from_entity(color),
            message="Color already exists"
        )

    color = Color(
        code=req.code,
        name=req.name,
        highlight=req.highlight
    )
    session.add(color)
    await session.commit()
    return ColorResponse(
        data=ColorDataResponse.from_entity(color),
        message="Color created successfully"
    )


async def update_color(color_id: str, req: ColorRequest, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == color_id)
    result = await session.execute(stmt)
    color = result.scalars().first()

    if color is None:
        return ColorResponse(
            data=None,
            message="Color not found"
        )

    color.code = req.code
    color.name = req.name
    color.highlight = req.highlight
    await session.commit()
    return ColorResponse(
        data=ColorDataResponse.from_entity(color),
        message="Color updated successfully"
    )


async def delete_color(color_id: str, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == color_id)
    result = await session.execute(stmt)
    color = result.scalars().first()

    if color is None:
        return ColorResponse(
            data=None,
            message="Color not found"
        )

    await session.delete(color)
    await session.commit()
    return ColorResponse(
        data=ColorDataResponse.from_entity(color),
        message="Color deleted successfully"
    )
