from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import EmailStr, BaseModel

from app.constants.roles import Roles
from app.responses.base import BaseResponse


class UserDataResponse(BaseModel):
    id: UUID | str
    username: str
    email: EmailStr
    is_active: bool
    role: str
    created_at: Optional[Union[str, datetime]] = None

    @classmethod
    def from_entity(cls, user):
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            role=Roles.get_name(user.role),
            created_at=user.created_at
        )


class UserResponse(BaseResponse):
    data: UserDataResponse | None


class UserListResponse(BaseResponse):
    data: list[UserDataResponse] | None
