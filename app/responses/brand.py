from uuid import UUID

from pydantic import BaseModel

from app.models.brand import Brand
from app.responses.base import BaseResponse


class BrandDataResponse(BaseModel):
    id: str | UUID
    name: str
    description: str | None
    attachment: str | None

    @classmethod
    def from_entity(cls, brand: 'Brand') -> 'BrandDataResponse':
        if brand is None:
            return cls(
                id="",
                name="",
                description="",
                attachment=""
            )

        return cls(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            attachment=brand.attachment
        )


class BrandResponse(BaseResponse):
    data: BrandDataResponse | None

    @classmethod
    def from_entity(cls, brand: 'Brand') -> 'BrandResponse':
        if brand is None:
            return cls(
                data=None,
                message="Brand not found"
            )

        return cls(
            data=BrandDataResponse.from_entity(brand),
            message="Brand fetched successfully"
        )


class BrandListResponse(BaseResponse):
    data: list[BrandDataResponse]

    @classmethod
    def from_entities(cls, brands: list['Brand']) -> 'BrandListResponse':
        return cls(
            data=[BrandDataResponse.from_entity(brand) for brand in brands],
            message="Brands fetched successfully"
        )
