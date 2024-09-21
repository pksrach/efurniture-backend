from uuid import UUID
from pydantic import BaseModel
from app.models.location import Location
from app.responses.base import BaseResponse


class LocationDataResponse(BaseModel):
    id: str | UUID
    name: str
    price: float
    parent_id: str | UUID | None
    children: list['LocationDataResponse']

    @classmethod
    def from_entity(cls, location: 'Location') -> 'LocationDataResponse':
        if location is None:
            return cls(
                id="",
                name="",
                price=0.0,
                parent_id=None,
                children=[]
            )

        return cls(
            id=location.id,
            name=location.name,
            price=float(location.price),  # Ensure that price is returned as float
            parent_id=location.parent_id,
            children=[cls.from_entity(child) for child in (location.children or [])]
        )


class LocationResponse(BaseResponse):
    data: LocationDataResponse | None

    @classmethod
    def from_entity(cls, location: 'Location') -> 'LocationResponse':
        if location is None:
            return cls(
                data=None,
                message="Location not found"
            )

        return cls(
            data=LocationDataResponse.from_entity(location),
            message="Location fetched successfully"
        )


class LocationListResponse(BaseResponse):
    data: list[LocationDataResponse]

    @classmethod
    def from_entities(cls, locations: list['Location']) -> 'LocationListResponse':
        return cls(
            data=[LocationDataResponse.from_entity(location) for location in locations],
            message="Locations fetched successfully"
        )
