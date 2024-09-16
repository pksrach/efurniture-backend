from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.color import Color
from app.responses.color import ColorListResponse, ColorDataResponse, ColorResponse
from app.schemas.color import ColorRequest

settings = get_settings()


async def get_colors(session: AsyncSession) -> ColorListResponse:
    stmt = select(Color).order_by(Color.created_at.desc())
    result = await session.execute(stmt)
    colors = result.scalars().all()
    return ColorListResponse.from_entities(colors)


async def get_color(id: str, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == id)
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


async def update_color(id: str, req: ColorRequest, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == id)
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


async def delete_color(id: str, session: AsyncSession) -> ColorResponse:
    stmt = select(Color).where(Color.id == id)
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
