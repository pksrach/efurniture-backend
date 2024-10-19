from uuid import UUID

from pydantic import BaseModel

from app.responses.base import BaseResponse


class ColorDataResponse(BaseModel):
    id: str | UUID
    code: str | None
    name: str
    highlight: str | None

    @classmethod
    def from_entity(cls, color) -> 'ColorDataResponse':
        if color is None:
            return cls(
                id="",
                code="",
                name="",
                highlight=""
            )

        return cls(
            id=color.id,
            code=color.code,
            name=color.name,
            highlight=color.highlight
        )


class ColorResponse(BaseResponse):
    data: ColorDataResponse | None

    @classmethod
    def from_entity(cls, color):
        if color is None:
            return cls(data=None, message="Color not found")

        return cls(
            data=ColorDataResponse.from_entity(color),
            message="Color fetched successfully"
        )


class ColorListResponse(BaseResponse):
    data: list[ColorDataResponse]

    @classmethod
    def from_entities(cls, colors):
        return cls(
            data=[ColorDataResponse.from_entity(color) for color in colors],
            message="Colors fetched successfully"
        )
