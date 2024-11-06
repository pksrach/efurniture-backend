from uuid import UUID

from pydantic import BaseModel


class KeyValueResponse(BaseModel):
    key: str | UUID | None
    value: str | None