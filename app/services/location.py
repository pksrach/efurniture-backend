from sqlalchemy.exc import IntegrityError
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import get_settings
from app.models.location import Location
from app.schemas.location import LocationRequest
from app.responses.location import Location,LocationDataResponse,LocationListResponse,LocationResponse
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

async def _get_location_by_id(id: str, session: AsyncSession) -> Optional[Location]:
    stmt = select(Location).where(Location.id == id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

async def get_locations(session: AsyncSession) -> LocationListResponse:
    stmt = select(Location).order_by(Location.created_at.desc())
    result = await session.execute(stmt)
    locations = result.scalars().all()
    return LocationListResponse.from_entities(list(locations))

async def get_location(id: str, session: AsyncSession) -> LocationResponse:
    location = await _get_location_by_id(id, session)

    if location is None:
        logger.warning(f"Location with ID {id} not found.")
        return LocationResponse(
            data=None,
            message="Location not found"
        )
    return LocationResponse.from_entity(location)

async def create_location(req: LocationRequest, session: AsyncSession) -> LocationResponse:
    """Create a new location with the provided data."""
    # Optionally check if a location with the same name exists
    location = Location(
        name=req.name,
        price=req.price,
        parent_id=req.parent_id
    )

    try:
        session.add(location)
        await session.commit()
        await session.refresh(location)
        logger.info(f"location '{req.name}' created successfully.")
        return LocationResponse(
            data=LocationDataResponse.from_entity(location),
            message="location created successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during creation of location: {str(e)}")
        return LocationResponse(
            data=None,
            message="Failed to create location due to database integrity error."
        )

async def update_location(id: str, req: LocationRequest, session: AsyncSession) -> LocationResponse:
    """Update a Location by ID with the provided data."""
    location = await _get_location_by_id(id, session)

    if location is None:
        logger.warning(f"Location with ID {id} not found.")
        return LocationResponse(
            data=None,
            message="Location not found"
        )

    update_data = req.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(location, key, value)

    try:
        await session.commit()
        await session.refresh(location)
        logger.info(f"Location with ID {id} updated successfully.")
        return LocationResponse(
            data=LocationDataResponse.from_entity(location),
            message="Location updated successfully"
        )
    except IntegrityError as e:
        await session.rollback()
        logger.error(f"Integrity error during update of Location {id}: {str(e)}")
        return LocationResponse(
            data=None,
            message="Failed to update Location due to database integrity error."
        )

async def delete_location(id: str, session: AsyncSession)-> LocationResponse:
    stmt = select(Location).where(Location.id == id)
    result = await session.execute(stmt)
    location = result.scalar()

    if location is None:
        return LocationResponse(
            data=None,
            message="Location not found"
        )
    
    await session.delete(location)
    await session.commit()
    return LocationResponse(
        data=LocationDataResponse.from_entity(location),
        message="Location deleted successfully"
    )